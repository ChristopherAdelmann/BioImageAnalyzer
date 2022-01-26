import concurrent.futures
from typing import List, Tuple

import numpy as np
import pandas as pd
import skimage.color as color
import skimage.filters as filters
import skimage.measure as measure
from models.analysis_results.cell_isolation_analysis_result import (
    Cell_Isolation_Analysis_Result,
)
from models.image.image_model import Image_Model
from scipy.ndimage.morphology import binary_fill_holes

from .abstract_analysis_method import Analysis_Method


class Cell_Isolation_Analysis(Analysis_Method):
    @staticmethod
    def calculate(image_models: List[Image_Model]) -> Cell_Isolation_Analysis_Result:

        result_image_models: List[Image_Model] = []
        labeled_image_models: List[Image_Model] = []
        pixel_areas: List[int] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(
                Cell_Isolation_Analysis._calculate_single_image, image_models
            )

            for i, result in enumerate(results):
                result_image_models.append(
                    Image_Model.from_other_image_model(image_models[i], result[0])
                )
                labeled_image_models.append(
                    Image_Model.from_other_image_model(image_models[i], result[1])
                )
                pixel_areas.append(result[2])

        print("Write Results")
        pd.DataFrame(
            pixel_areas,
            index=list(map(lambda res: res.image_description, result_image_models)),
            columns=["Cell Area [px]"],
        )

        return Cell_Isolation_Analysis_Result(
            pd.DataFrame(),
            result_image_models,
            labeled_image_models,
        )

    @staticmethod
    def _calculate_single_image(
        image_model: Image_Model,
    ) -> Tuple[np.ndarray, np.ndarray, int]:
        """Computes the cell isolation result for a given image model

        Args:
            image_model (Image_Model): The given image model

        Returns:
            Tuple[np.ndarray, np.ndarray, int]: (color marked image data, labeled image data, area_pixel_count)
        """
        print("Started Process")
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
        otsu_thresh = filters.threshold_triangle(working_image_data)
        # Applying threshold to image data
        working_image_data = working_image_data > otsu_thresh
        # Inverting image data for filling holes
        working_image_data = np.invert(working_image_data)
        # Filling holes in image data
        working_image_data = binary_fill_holes(working_image_data)
        # Label connected components in image data
        working_image_data = measure.label(working_image_data)
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
        print("Finished Analysis")
        return (result_image_data, labeled_image_data, pixel_area)
