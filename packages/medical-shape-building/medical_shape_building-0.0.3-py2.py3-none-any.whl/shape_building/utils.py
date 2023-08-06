import os
from typing import Sequence, Union

import numpy as np
import torch
import torchio as tio
from medical_shape.shape import SHAPE
from skimage.measure import label


def save_subject(path: str, subject: tio.data.Subject, exist_ok: bool = True):

    os.makedirs(path, exist_ok=exist_ok)
    extensions = {
        tio.constants.LABEL: ".nii.gz",
        tio.constants.INTENSITY: ".nii.gz",
        SHAPE: ".mjson",
    }
    for k, v in subject.get_images_dict(intensity_only=False).items():
        v.save(os.path.join(path, k.replace("/", "_") + extensions[v.type]))


def detect_out_of_bound_landmarks(
    landmarks: torch.Tensor,
    image_shape: Union[Sequence[int], torch.Tensor],
    boundary_margin: int = 0,
):
    curr_indices = torch.nonzero(
        (
            (landmarks < boundary_margin)
            + torch.stack(
                [
                    landmarks[..., i] >= image_shape[-(i + 1)] - boundary_margin
                    for i in range(landmarks.size(-1))
                ],
                -1,
            )
        ).sum(-1)
    )

    return curr_indices.view(-1).tolist()


def get_largest_cc(mask: torch.Tensor) -> torch.Tensor:
    labels = label(mask.cpu().detach()[0].numpy())
    assert labels.max() != 0  # assume at least 1 CC
    largest_cc = labels == np.argmax(np.bincount(labels.flat)[1:]) + 1
    return torch.from_numpy(largest_cc).to(mask)[None]
