import ntpath
import uuid

import numpy as np

from models.abstract_identifiable_image import Identifiable_Image


class Base_Image_Model:
    def __init__(
        self,
        image_path: str,
        image_data: np.ndarray,
        slice_index: int,
        slice_count: int,
    ):
        self.base_image_path: str = image_path
        self.image_data: np.ndarray = image_data
        self.image_name: str = ntpath.basename(image_path)
        self.slice_index: int = slice_index
        self.total_slice_count: int = slice_count
        self.image_uuid = uuid.uuid4()

    @property
    def image_description(self) -> str:
        return (
            f"{self.image_name} (Slice {self.slice_index} of {self.total_slice_count})"
        )


class Result_Image_Model:
    def __init__(self, base_image_model: Identifiable_Image, image_data: np.ndarray):
        self.base_image_path: str = base_image_model.base_image_path
        self.image_name: str = base_image_model.image_name
        self.slice_index: int = base_image_model.slice_index
        self.total_slice_count: int = base_image_model.total_slice_count
        self.image_uuid = base_image_model.image_uuid
        self.image_data: np.ndarray = image_data

    @classmethod
    def copy_base_image_model(
        cls, base_image_model: Identifiable_Image
    ) -> "Result_Image_Model":
        return cls(base_image_model, base_image_model.image_data)

    @property
    def image_description(self) -> str:
        return f"Image: {self.image_name} (Slice {self.slice_index} of {self.total_slice_count})"
