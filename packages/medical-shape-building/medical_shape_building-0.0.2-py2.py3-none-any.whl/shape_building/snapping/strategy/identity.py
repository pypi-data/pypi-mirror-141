import torch

from shape_building.snapping.strategy.base import SnappingStrategy


class IdentitySnappingStrategy(SnappingStrategy):
    def get_snapped_points(
        self, mask: torch.Tensor, points: torch.Tensor
    ) -> torch.Tensor:
        return points
