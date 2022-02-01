import math
from typing import List, Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skimage.color as color
import skimage.morphology as morph
from models.analysis_results.largest_component_roughness_analysis_result import (
    Largest_Component_Roughness_Analysis_Result,
)
from models.image.image_model import Image_Model
from skimage.measure import regionprops

from analysis_tools.threshold_options import Threshold_Options

from .largest_component_isolation_analysis_method import (
    Largest_Component_Isolation_Analysis,
)


class Largest_Component_Roughness_Analysis:
    @staticmethod
    def calculate(
        image_models: List[Image_Model],
        thresh_option: Threshold_Options = Threshold_Options.yen,
    ) -> Largest_Component_Roughness_Analysis_Result:
        """Analysis for the roughness of the largest connected component within the image datas.
        
        Must be called asynchronously.

        Args:
            image_models (List[Image_Model]): The image models to analyse.
            thresh_option (Threshold_Options, optional): The threshold option for the analysis. Defaults to Threshold_Options.yen.

        Returns:
            Largest_Component_Roughness_Analysis_Result: The finished analysis result.
        """
        isolated_cell_result = Largest_Component_Isolation_Analysis.calculate(
            image_models, thresh_option
        )

        centroids = tuple(
            regionprops(res.image_data)[0].centroid
            for res in isolated_cell_result.labeled_image_models
        )

        # Converts the labeled images data to binary image.
        binary_masks_data = (
            labeled_image_data.image_data.copy() >= 1
            for labeled_image_data in isolated_cell_result.labeled_image_models
        )

        edge_masks_data = tuple(
            np.bitwise_xor(binary_data, morph.binary_erosion(binary_data))
            for binary_data in binary_masks_data
        )

        edge_masks_pixels_coords: List[Tuple[Tuple[int, int], ...]] = []
        for edge_mask_data in edge_masks_data:
            y_coords, x_coords = np.where(edge_mask_data == True)
            coords_in_mask = tuple(zip(y_coords, x_coords))
            edge_masks_pixels_coords.append(coords_in_mask)

        edge_masks_pixels_dists_to_centroid: List[Tuple[float, ...]] = []
        for i, mask_coords in enumerate(edge_masks_pixels_coords):
            dists = tuple(
                Largest_Component_Roughness_Analysis._distance(coord, centroids[i])
                for coord in mask_coords
            )
            edge_masks_pixels_dists_to_centroid.append(dists)

        edge_masks_pixels_dists_to_centroid_stdev = tuple(
            np.std(dists) for dists in edge_masks_pixels_dists_to_centroid
        )
        edge_masks_pixels_dists_to_centroid_mean = tuple(
            np.mean(dists) for dists in edge_masks_pixels_dists_to_centroid
        )

        roundness: List[float] = []
        for i in range(len(edge_masks_pixels_dists_to_centroid)):
            norm_stdev = (
                edge_masks_pixels_dists_to_centroid_stdev[i]
                / edge_masks_pixels_dists_to_centroid_mean[i]
            )
            roundness.append(norm_stdev)

        for i, edge_mask_data in enumerate(edge_masks_data):
            edge_mask_data = morph.binary_dilation(edge_mask_data)
            edge_mask_data[edge_mask_data == True] = 1

        result_images_data = tuple(
            color.label2rgb(edge_mask_data, image_models[i].image_data, alpha=0.5)
            for i, edge_mask_data in enumerate(edge_masks_data)
        )

        for i, image_data in enumerate(result_images_data):
            cv2.circle(
                image_data,
                (round(centroids[i][1]), round(centroids[i][0])),
                5,
                (255, 0, 0),
                thickness=cv2.FILLED,
            )

        index_names = tuple(
            map(lambda res: res.image_uuid, isolated_cell_result.result_image_models)
        )

        base_image_names = tuple(
            image_model.image_description
            for image_model in isolated_cell_result.result_image_models
        )

        result_df = pd.DataFrame(
            base_image_names,
            index=index_names,
            columns=["Base Image Name"],
        )

        result_df["Centroid [idx_y, idx_x]"] = centroids
        result_df[
            "Edge Pixel Distance To Centroid STDEV [px]"
        ] = edge_masks_pixels_dists_to_centroid_stdev
        result_df[
            "Edge Pixel Distance To Centroid MEAN [px]"
        ] = edge_masks_pixels_dists_to_centroid_mean
        result_df["Normalized Roundness"] = roundness

        result_image_models = list(
            Image_Model.from_other_image_model(
                isolated_cell_result.result_image_models[i], image_data
            )
            for i, image_data in enumerate(result_images_data)
        )

        print("Result Data:", result_df)

        return Largest_Component_Roughness_Analysis_Result(
            result_df, result_image_models
        )

    @staticmethod
    def _distance(pointA: Tuple[int, int], pointB: Tuple[float, float]) -> float:
        dx = pointB[0] - pointA[0]
        dy = pointB[1] - pointA[1]
        res: float = math.sqrt((pow(dx, 2) + pow(dy, 2)))
        return res
