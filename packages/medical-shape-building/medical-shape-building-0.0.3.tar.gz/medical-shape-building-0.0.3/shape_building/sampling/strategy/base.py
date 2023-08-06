from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class SamplingStrategy(ABC):
    """Abstract Base Class defining how points on the mask surface are sampled."""

    @abstractmethod
    def get_sampling_points(
        self, masked_image: np.ndarray, number_of_points: int, *args, **kwargs
    ) -> np.ndarray:
        pass

    def __call__(self, *args, **kwargs):
        return self.get_sampling_points(*args, **kwargs)
