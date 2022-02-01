import concurrent.futures
from itertools import repeat
from typing import Any, List, Tuple, cast

import numpy as np
import pandas as pd
import skimage.color as color
import skimage.measure as measure
from models.analysis_results.largest_component_isolation_analysis_result import (
    Largest_Component_Isolation_Analysis_Result,
)
from models.image.image_model import Image_Model
from scipy.ndimage.morphology import binary_fill_holes

from .threshold_options import Threshold_Options


class Largest_Component_Isolation_Analysis:
    @staticmethod
    def calculate(
        image_models: List[Image_Model],
        thresh_option: Threshold_Options = Threshold_Options.otsu,
    ) -> Largest_Component_Isolation_Analysis_Result:
        """Calculates the largest component of the given image image_models

        Must be called asynchronously.

        Args:
            image_models (List[Image_Model]): The image models to analyse.
            thresh_option (Threshold_Options, optional): The threshold option for the analysis. Defaults to Threshold_Options.otsu.

        Returns:
            Largest_Component_Isolation_Analysis_Result: The result of the analysis.
        """
        result_image_models: List[Image_Model] = []
        labeled_image_models: List[Image_Model] = []
        pixel_areas: List[int] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(
                Largest_Component_Isolation_Analysis._calculate_single_image,
                image_models,
                repeat(thresh_option),
            )

            for i, result in enumerate(results):
                result_image_models.append(
                    Image_Model.from_other_image_model(image_models[i], result[0])
                )
                labeled_image_models.append(
                    Image_Model.from_other_image_model(image_models[i], result[1])
                )
                pixel_areas.append(result[2])

        pd.DataFrame(
            pixel_areas,
            index=list(map(lambda res: res.image_description, result_image_models)),
            columns=["Cell Area [px]"],
        )

        return Largest_Component_Isolation_Analysis_Result(
            pd.DataFrame(),
            result_image_models,
            labeled_image_models,
        )

    @staticmethod
    def _calculate_single_image(
        image_model: Image_Model, thresh_option: Threshold_Options
    ) -> Tuple[np.ndarray, np.ndarray, int]:
        """Computes the largest component isolation result for a given image model

        Args:
            image_model (Image_Model): The given image model

        Returns:
            Tuple[np.ndarray, np.ndarray, int]: (color marked image data, labeled image data, area_pixel_count)
        """
        working_image_data: np.ndarray
        pixel_values = 1
        image_data_shape = image_model.image_data.shape
        if len(image_data_shape) > 2:
            pixel_values = image_data_shape[2]
        if pixel_values == 1:
            working_image_data = image_model.image_data.copy()
        else:
            working_image_data = color.rgb2gray(image_model.image_data.copy())
        # Calculating threshold
        thresh = thresh_option.thresh_value(working_image_data)
        # Applying threshold to image data
        working_image_data = working_image_data > thresh
        # Inverting image data for filling holes
        working_image_data = np.invert(working_image_data)
        # Filling holes in image data
        working_image_data = cast(
            np.ndarray[Any, Any], binary_fill_holes(working_image_data)
        )
        # Label connected components in image data
        working_image_data = measure.label(working_image_data)  # type: ignore
        # Get bin counts and calculate max size labels
        image_bin_counts = np.bincount(working_image_data.flatten())
        image_max_label = np.delete(image_bin_counts, 0).argmax() + 1
        # Setting all non max labels to zero
        working_image_data[working_image_data != image_max_label] = 0
        # Setting labels to one
        working_image_data[working_image_data == image_max_label] = 1

        labeled_image_data = working_image_data

        result_image_data = color.label2rgb(working_image_data, image_model.image_data)

        pixel_area = np.count_nonzero(labeled_image_data == 1)
        return (result_image_data, labeled_image_data, pixel_area)
