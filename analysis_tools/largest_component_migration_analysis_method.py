import copy
import math
import time
from types import NoneType
from typing import List, Tuple, cast

import cv2
import pandas as pd
from models.analysis_results.largest_component_migration_analysis_result import (
    Largest_Component_Migration_Analysis_Result,
)
from models.image.image_model import Image_Model
from skimage.measure import regionprops

from .abstract_analysis_method import Analysis_Method_Protocol
from .largest_component_isolation_analysis_method import (
    Largest_Component_Isolation_Analysis,
)
from .threshold_options import Threshold_Options


class Largest_Component_Migration_Analysis:
    @staticmethod
    def calculate(
        image_models: List[Image_Model],
        thresh_option: Threshold_Options = Threshold_Options.triangle,
    ) -> Largest_Component_Migration_Analysis_Result:
        """Analysis for the migration of the largest connected component within the image datas.

        Must be called asynchronously.

        Args:
            image_models (List[Image_Model]): List of image models for analysis.
            thresh_option (Threshold_Options, optional): The threshold option for the analysis. Defaults to Threshold_Options.yen.

        Returns:
            Cell_Migration_Analysis_Result: The finished analysis result.
        """

        isolated_cell_result = Largest_Component_Isolation_Analysis.calculate(
            image_models, thresh_option
        )

        # Extracting the props of the largest connected component over all isolated cell results
        props_for_results = tuple(
            regionprops(res.image_data)[0]
            for res in isolated_cell_result.labeled_image_models
        )

        distances_to_prev_centroid: List[float | None] = [None]
        migration_lines_points: List[
            Largest_Component_Migration_Analysis.Line_Points | None
        ] = [None]

        # Preparing the result image model for the first image without draw
        result_image_models: List[Image_Model] = [
            copy.copy(isolated_cell_result.result_image_models[0])
        ]

        # Iterate over all centroids and calculate traveled distance to previous centroid
        for i in range(1, len(props_for_results)):
            prev_centroid: Tuple[float, float] = props_for_results[i - 1].centroid
            curr_centroid: Tuple[float, float] = props_for_results[i].centroid

            dist = Largest_Component_Migration_Analysis.distance(
                prev_centroid, curr_centroid
            )
            distances_to_prev_centroid.append(dist)

            line_start_coord = (round(prev_centroid[1]), round(prev_centroid[0]))
            line_end_coord = (round(curr_centroid[1]), round(curr_centroid[0]))
            migration_lines_points.append(
                Largest_Component_Migration_Analysis.Line_Points(
                    line_start_coord, line_end_coord
                )
            )

            # Drawing the previous path on each frame
            curr_image_model = isolated_cell_result.result_image_models[i]

            for j in range(0, i + 1):
                line_points = migration_lines_points[j]
                if type(line_points) != NoneType:
                    line_points = cast(
                        Largest_Component_Migration_Analysis.Line_Points, line_points
                    )
                    cv2.line(
                        curr_image_model.image_data,
                        line_points.start_point,
                        line_points.end_point,
                        (255, 0, 0),
                        thickness=4,
                    )

            result_image_models.append(curr_image_model)

        # Write dataframe with
        index_names = tuple(
            map(lambda res: res.image_uuid, isolated_cell_result.result_image_models)
        )

        base_image_names = tuple(
            map(
                lambda res: res.image_description,
                isolated_cell_result.result_image_models,
            )
        )

        result_df = pd.DataFrame(
            base_image_names,
            index=index_names,
            columns=["Base Image Name"],
        )

        result_df["Migration Distance [px]"] = distances_to_prev_centroid

        result_df["Centroid [idx_y, idx_x]"] = tuple(
            props.centroid for props in props_for_results
        )

        result_df["Area [px]"] = tuple(props.area for props in props_for_results)

        return Largest_Component_Migration_Analysis_Result(
            result_df, result_image_models
        )

    @staticmethod
    def distance(pointA: Tuple[float, float], pointB: Tuple[float, float]) -> float:
        dx = pointB[0] - pointA[0]
        dy = pointB[1] - pointA[1]
        res = math.sqrt((pow(dx, 2) + pow(dy, 2)))
        return res

    class Line_Points(object):
        def __init__(self, start_point: Tuple[int, int], end_point: Tuple[int, int]):
            self.start_point = start_point
            self.end_point = end_point
