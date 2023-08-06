import numpy as np

from shape_building.sampling.strategy.base import SamplingStrategy
from shape_building.sampling.strategy.manual import ManualSamplingStrategy


class SemiManualSamplingStrategy(SamplingStrategy):
    def __init__(
        self,
        automatic_sampling: SamplingStrategy,
        manual_sampling: ManualSamplingStrategy,
    ):
        super().__init__()
        self.automatic_sampling = automatic_sampling
        self.manual_sampling = manual_sampling

    def get_sampling_points(
        self, masked_image: np.ndarray, number_of_points: int, *args, **kwargs
    ) -> np.ndarray:
        manual_points = self.manual_sampling(masked_image, None)
        assert len(manual_points) <= number_of_points

        automatic_points = self.automatic_sampling(
            masked_image, number_of_points - len(manual_points)
        )

        total_points = np.concatenate((manual_points, automatic_points))
        return total_points
