import uuid
from typing import Protocol

import numpy as np


class Identifiable_Image(Protocol):
    base_image_path: str
    image_data: np.ndarray
    image_name: str
    slice_index: int
    total_slice_count: int
    image_uuid: uuid.UUID

    @property
    def image_description(self) -> str:
        ...
