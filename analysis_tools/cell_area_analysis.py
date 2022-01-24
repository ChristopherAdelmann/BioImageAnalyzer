from typing import List

import numpy as np
import skimage.color as color
import skimage.filters as filters
import skimage.measure as measure
from models.base_image_model import Base_Image_Model
from scipy.ndimage.morphology import binary_fill_holes


class Cell_Area_Analysis:
    @staticmethod
    def calculate(image_models: List[Base_Image_Model]):

        working_images_data: List[np.ndarray] = []

        for image_model in image_models:
            pixel_values = 1
            image_data_shape = image_model.image_data.shape

            if len(image_data_shape) > 2:
                pixel_values = image_data_shape[2]

            if pixel_values == 1:
                working_images_data.append(image_model.image_data.copy())
            else:
                working_images_data.append(
                    color.rgb2gray(image_model.image_data.copy())
                )

        # Calculating otsu thresh
        otsu_thresh = tuple(filters.threshold_otsu(i) for i in working_images_data)

        # Applying threshold to image data
        working_images_data = list(
            working_images_data[i] > otsu_thresh[i] for i in range(len(otsu_thresh))
        )

        # Inverting image data for filling holes
        working_images_data = list(np.invert(img) for img in working_images_data)

        # Filling holes in image data
        working_images_data = list(
            binary_fill_holes(img) for img in working_images_data
        )

        # Label connected components in image data
        working_images_data = list(measure.label(img) for img in working_images_data)

        # Get bin counts and calculate max size labels
        images_bin_counts = tuple(
            np.bincount(labels.flatten()) for labels in working_images_data
        )
        images_max_label = tuple(
            np.delete(bin_counts, 0).argmax() + 1 for bin_counts in images_bin_counts
        )

        # Setting all non max labels to zero
        for i in range(len(images_max_label)):
            img = working_images_data[i]
            max_label = images_max_label[i]

            img[img != max_label] = 0
            working_images_data[i] = img

        # Color label original image data
        annotated_images_data = tuple(
            color.label2rgb(working_images_data[i], image_models[i].image_data)
            for i in range(len(working_images_data))
        )

        # fig, ax = plt.subplots()

        # ax.imshow(annotated_images_data[0])


# path = "/Volumes/NO NAME/raw data/VID665_D3_1_03d08h00m.tif"
# test_images_model = [Base_Image_Model(path)]

# Cell_Area_Analysis.calculate(test_images_model)

# plt.show()
