import logging
from typing import Optional, Sequence, Union

import torch
import torchio as tio
from medical_shape import Shape

from medical_shape_building.airlab import (
    RegistrationImage,
    affine_multiscale_demons_registration,
    transform_points,
)
from medical_shape_building.snapping import SnappingStrategies
from medical_shape_building.snapping.snapper import PointSnapper
from medical_shape_building.utils import detect_out_of_bound_landmarks

_logger = logging.getLogger(__name__)


def transfer_landmarks_by_registration(
    target_image: Union[RegistrationImage, tio.data.Image],
    source_image: Union[RegistrationImage, tio.data.Image],
    landmarks: Shape,
    learning_rate_affine: float = 0.05,
    num_iterations_affine: int = 75,
    learning_rates_demons: Sequence[float] = (0.1, 0.1, 0.01),
    num_iterations_demons: Sequence[int] = (80, 40, 20),
    shrink_factors_demons: Sequence[Sequence[int]] = ((4, 4, 4), (2, 2, 2)),
    sigmas_demons: Sequence[Sequence[int]] = ((3, 3, 3), (3, 3, 3), (3, 3, 3)),
    snapping_strategy: str = "identity",
    device: Optional[Union[str, torch.device]] = None,
    landmarks_zyx: bool = False,
    boundary_margin_oob_detection: int = 0,
    **demons_kwargs,
):
    (
        warped_image,
        displacement_field,
        dice_coefficient,
    ) = affine_multiscale_demons_registration(
        # Switch images on purpose since SimpleITK interpolates the other way around
        target_image=source_image,
        source_image=target_image,
        learning_rate_affine=learning_rate_affine,
        num_iterations_affine=num_iterations_affine,
        learning_rates_demons=learning_rates_demons,
        num_iterations_demons=num_iterations_demons,
        shrink_factors_demons=shrink_factors_demons,
        sigmas_demons=sigmas_demons,
        device=device,
        **demons_kwargs,
        # TODO: Remove this after debugging
        points=landmarks,
    )

    transformed_landmarks = Shape(
        tensor=transform_points(
            landmarks.tensor, displacement_field, zyx=landmarks_zyx
        ),
        affine=target_image.to_torchio().affine
        if isinstance(target_image, RegistrationImage)
        else target_image.affine,
    )

    _logger.info(f"Snapping Landmarks to mask with {snapping_strategy}")
    if isinstance(target_image, RegistrationImage):
        image_shape = target_image.to_torchio().spatial_shape
    else:
        image_shape = target_image.spatial_shape
    out_of_bound_indices = detect_out_of_bound_landmarks(
        transformed_landmarks.tensor,
        image_shape,
        boundary_margin=boundary_margin_oob_detection,
    )
    snapper = PointSnapper(
        SnappingStrategies.from_str(snapping_strategy).value(
            points_xyz=not landmarks_zyx
        )
    )

    transformed_landmarks.set_data(
        snapper(
            warped_image.image.to(device), transformed_landmarks.tensor.to(device)
        ).cpu()
    )

    return (
        transformed_landmarks,
        warped_image,
        displacement_field,
        dice_coefficient,
        out_of_bound_indices,
    )
