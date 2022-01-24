import math
from types import NoneType
from typing import List, Tuple, cast

import cv2
import matplotlib.pyplot as plt
import pandas as pd
from models.base_image_model import Result_Image_Model
from models.cell_isolation_analysis_result import Cell_Isolation_Analysis_Result
from models.cell_migration_analysis_result import Cell_Migration_Analysis_Result
from skimage.measure import regionprops


class Cell_Migration_Analysis:
    @staticmethod
    def calculate(
        isolated_cell_results: List[Cell_Isolation_Analysis_Result],
    ) -> Cell_Migration_Analysis_Result:

        props_for_results = tuple(
            regionprops(res.labeled_image_data)[0] for res in isolated_cell_results
        )
        distances_to_prev_centroid: List[float | None] = [None]
        migration_lines_points: List[Cell_Migration_Analysis.Line_Points | None] = [
            None
        ]
        result_image_models: List[Result_Image_Model] = [
            Result_Image_Model.copy_base_image_model(
                isolated_cell_results[0].result_image_model
            )
        ]

        for i in range(1, len(props_for_results)):
            prev_centroid: Tuple[float, float] = props_for_results[i - 1].centroid
            curr_centroid: Tuple[float, float] = props_for_results[i].centroid

            dist = Cell_Migration_Analysis.distance(prev_centroid, curr_centroid)
            distances_to_prev_centroid.append(dist)

            line_start_coord = (round(prev_centroid[1]), round(prev_centroid[0]))
            line_end_coord = (round(curr_centroid[1]), round(curr_centroid[0]))
            migration_lines_points.append(
                Cell_Migration_Analysis.Line_Points(line_start_coord, line_end_coord)
            )
            curr_image_model = isolated_cell_results[i].result_image_model

            for j in range(0, i + 1):
                print("Image Loop:", i)
                line_points = migration_lines_points[j]
                if type(line_points) != NoneType:
                    print("Image Line:", i, j)
                    line_points = cast(Cell_Migration_Analysis.Line_Points, line_points)
                    cv2.line(
                        curr_image_model.image_data,
                        line_points.start_point,
                        line_points.end_point,
                        (255, 0, 0),
                        thickness=4,
                    )

            result_image_models.append(curr_image_model)

        index_names = tuple(
            map(lambda res: res.result_image_model.image_uuid, isolated_cell_results)
        )

        base_image_names = tuple(
            map(
                lambda res: res.result_image_model.image_description,
                isolated_cell_results,
            )
        )

        result_df = pd.DataFrame(
            base_image_names,
            index=index_names,
            columns=["Base Image Name"],
        )

        result_df["Migration Distance [px]"] = distances_to_prev_centroid

        result_df["Centroid [idx_y, idx_x]"] = tuple(
            map(lambda props: props.centroid, props_for_results)
        )

        result_df["Area [px]"] = tuple(map(lambda props: props.area, props_for_results))

        return Cell_Migration_Analysis_Result(result_df, result_image_models)

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
