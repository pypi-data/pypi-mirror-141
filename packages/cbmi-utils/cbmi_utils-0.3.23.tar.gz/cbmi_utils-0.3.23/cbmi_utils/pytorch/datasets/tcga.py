from pathlib import Path
from typing import Callable, Optional

from .h5_dataset import H5Dataset


TISSUE_TYPES = ['STAD', 'CRC_DX']
ALL_TISSUE_TYPES = ['all', *TISSUE_TYPES]


class TCGA(H5Dataset):
    """
    Data and further information can be found at https://zenodo.org/record/2530835
    """

    def __init__(
            self, root: Path, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None,
            num_samples: int = 1
    ):
        """
        Creates a new TCGA Dataset.
        """
        super().__init__(
            data_path=root,
            data_key='image',
            target_path=root,
            target_key='label',
            transform=transform,
            transform_target=transform_target,
            num_samples=num_samples
        )


def tcga_h5_224_split(
        subset: str, tissue_type: str = 'all', transform: Optional[Callable] = None,
        transform_target: Optional[Callable] = None, num_samples: int = 1
) -> TCGA:
    """
    This dataset consists of "train", "valid" and "test" dataset. The "valid" dataset is created by splitting 1/6 of the
    original "train" dataset.

    Args:
        subset: The subset to use. One of ["train", "valid", "test"]
        tissue_type: The tissue type to train on. One of ["all", "STAD", "CRC_DX"]. "all" combines all tissue types.
    """
    assert subset in ('train', 'valid', 'test')
    assert tissue_type in ALL_TISSUE_TYPES

    if subset in ('train', 'valid'):
        # in case of train or valid, we use the split dataset
        root = Path('/data/ldap/histopathologic/processed_read_only/TCGA/TOAD') / tissue_type / 'split' / f'{subset}.h5'
    else:
        # in case of test, we use the normal dataset
        root = Path('/data/ldap/histopathologic/processed_read_only/TCGA/TOAD') / tissue_type / f'{subset}.h5'
    return TCGA(root=root, transform=transform, transform_target=transform_target, num_samples=num_samples)


def tcga_h5_224_no_split(
        subset: str, tissue_type: str = 'all', transform: Optional[Callable] = None,
        transform_target: Optional[Callable] = None, num_samples: int = 1
) -> TCGA:
    """
    This dataset is only split into train and test dataset. Use "tcga_h5_224_split" in order to use "valid" dataset.

    Args:
        subset: The subset to use. One of ["train", "valid", "test"]
        tissue_type: The tissue type to train on. One of ["all", "STAD", "CRC_DX"]. "all" combines all tissue types.
    """
    assert subset in ('train', 'test'), '"tcga_h5_224" only supports "train" and "test" dataset. Use ' \
                                        '"tcga_h5_224_split" in order to use "valid" '
    assert tissue_type in ALL_TISSUE_TYPES
    root = Path('/data/ldap/histopathologic/processed_read_only/TCGA/TOAD') / tissue_type / f'{subset}.h5'

    return TCGA(root=root, transform=transform, transform_target=transform_target, num_samples=num_samples)
