import numpy as np
import pandas as pd
import skimage.color as color
import skimage.filters as filters
import skimage.measure as measure
from models.base_image_model import Base_Image_Model, Result_Image_Model
from models.cell_isolation_analysis_result import Cell_Isolation_Analysis_Result
from scipy.ndimage.morphology import binary_fill_holes


class Cell_Isolation_Analysis:
    @staticmethod
    def calculate(image_model: Base_Image_Model) -> Cell_Isolation_Analysis_Result:
        working_image_data: np.ndarray

        pixel_values = 1
        image_data_shape = image_model.image_data.shape

        if len(image_data_shape) > 2:
            pixel_values = image_data_shape[2]

        if pixel_values == 1:
            working_image_data = image_model.image_data.copy()
        else:
            working_image_data = color.rgb2gray(image_model.image_data.copy())

        # Calculating otsu thresh
        otsu_thresh = filters.threshold_otsu(working_image_data)

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

        # Color label original image data
        annotated_image_data = color.label2rgb(
            working_image_data, image_model.image_data
        )

        binary_image_data = working_image_data >= 1

        pixel_area = np.count_nonzero(binary_image_data == 1)

        pd.DataFrame(
            [pixel_area],
            index=[image_model.image_description],
            columns=["Cell Area [px]"],
        )

        return Cell_Isolation_Analysis_Result(
            pd.DataFrame(),
            Result_Image_Model(image_model, annotated_image_data),
            binary_image_data,
            working_image_data,
        )
