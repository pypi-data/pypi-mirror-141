from typing import Optional, Union

import SimpleITK as sitk
import torch

from medical_shape_building.airlab.image import RegistrationDisplacement


def transform_points_old(
    points: torch.Tensor,
    displacement: Union[RegistrationDisplacement, sitk.Image],
    zyx: bool = False,
):

    """Transforms a set of points with a displacement field.

    points (array): array of points displacement (SimpleITK.Image | Displacement ): displacement field to transform
    points return (array): transformed points
    """
    if isinstance(displacement, RegistrationDisplacement):
        displacement = displacement.to_itk()

    if isinstance(displacement, sitk.Image):
        df_transform = sitk.DisplacementFieldTransform(displacement)
    elif isinstance(displacement, sitk.DisplacementFieldTransform):
        df_transform = displacement
    else:
        raise TypeError(
            "displacement must be of type sitk.Image or "
            f"RegistrationDisplacement but found {type(displacement)}"
        )

    df_transform.SetSmoothingOff()

    if zyx:
        # flip from zyx to xyz
        points = torch.flip(points, (-1,))
    transformed_points = []
    for pt in points.tolist():
        transformed_points.append(df_transform.TransformPoint(pt))

    transformed_points = torch.tensor(
        transformed_points, device=points.device, dtype=points.dtype
    )

    if zyx:
        # flip back from xyz to zyx
        transformed_points = torch.flip(transformed_points, (-1,))

    return transformed_points


def transform_points(
    points: torch.Tensor,
    inverse_displacement_field: RegistrationDisplacement,
    current_image_shape: Optional[torch.Tensor] = None,
    **kwargs,
):
    dst_img_size = inverse_displacement_field.image_size.to(points)

    if current_image_shape is None:
        current_image_shape = dst_img_size
    elif not isinstance(current_image_shape, torch.Tensor):
        current_image_shape = torch.tensor(current_image_shape)

    current_image_shape = current_image_shape.to(points)

    from medical_shape.normalization import ShapeNormalization

    normalized_points = ShapeNormalization.normalize(points, current_image_shape)

    inv_disp_tensor = inverse_displacement_field.image[0].to(points)

    floored_pts = torch.floor(points)
    ceiled_pts = torch.ceil(points)
    floored_pts_list = floored_pts.long().tolist()
    ceiled_pts_list = ceiled_pts.long().tolist()

    factors_ceiled = ceiled_pts - points

    for idx in range(points.size(0)):

        # points outside the image don't have a defined displacement -> Skip them. They'll likely be clamped /discarded later anyway
        if (ceiled_pts[idx] >= dst_img_size).any():
            continue

        curr_disp_tensor_ceiled = inv_disp_tensor
        curr_disp_tensor_floored = inv_disp_tensor

        for i in range(points.size(-1)):
            curr_disp_tensor_floored = curr_disp_tensor_floored[
                :, floored_pts_list[idx][i]
            ]
            curr_disp_tensor_ceiled = curr_disp_tensor_ceiled[
                :, ceiled_pts_list[idx][i]
            ]

        curr_disp_tensor_ceiled = torch.flip(curr_disp_tensor_ceiled, (-1,))
        curr_disp_tensor_floored = torch.flip(curr_disp_tensor_floored, (-1,))

        normalized_points[idx] = (
            normalized_points[idx]
            + factors_ceiled[idx] * curr_disp_tensor_ceiled
            + (1 - factors_ceiled[idx]) * curr_disp_tensor_floored
        )

    transformed_points = ShapeNormalization.denormalize(normalized_points, dst_img_size)
    return transformed_points
