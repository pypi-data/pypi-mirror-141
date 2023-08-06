"""StarDist data[1]_ is a subset of DSB2018

.. [1] https://github.com/stardist/stardist/releases/download/0.1.0/dsb2018.zip
"""

import os.path
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union, Any

import albumentations
import cv2
import numpy as np
import tifffile

from ..base import MaskDataset
from ..types import BundledPath
from ..utils import imread_asarray, rle_decoding_inseg, read_csv, ordered_unique


class StarDist(MaskDataset):
    """Training set for StarDist [1]_, [2]_

    StarDist data is a subset of Data Science Bowl 2018 [3]_

    Find the nuclei in divergent images to advance medical discovery

    Parameters
    ----------
    root_dir : str
        Path to root directory
    output : {'both', 'image', 'mask'}, default: 'both'
        Change outputs. 'both' returns {'image': image, 'mask': mask}.
    transforms : albumentations.Compose, optional
        An instance of Compose (albumentations pkg) that defines augmentation in
        sequence.
    num_calls : int, optional
        Useful when ``transforms`` is set. Define the total length of the
        dataset. If it is set, it overwrites ``__len__``.
    grayscale : bool, default: False
        Convert images to grayscale
    grayscale_mode : {'cv2', 'equal', Sequence[float]}, default: 'cv2'
        How to convert to grayscale. If set to 'cv2', it follows opencv
        implementation. Else if set to 'equal', it sums up values along channel
        axis, then divides it by the number of expected channels.
    training : bool, default: True
        Load training set if True, else load testing one

    References
    ----------
    .. [1] https://arxiv.org/abs/1806.03535
    .. [2] https://github.com/stardist/stardist/releases/download/0.1.0/dsb2018.zip
    .. [3] https://www.kaggle.com/c/data-science-bowl-2018/

    See Also
    --------
    DSB2018
    MaskDataset : Super class
    Dataset : Base class
    DatasetInterface : Interface

    """
    # Set acronym
    acronym = 'StarDist'

    def __init__(
        self,
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_calls: Optional[int] = None,
        grayscale: bool = False,
        grayscale_mode: Union[str, Sequence[float]] = 'cv2',
        # specific to this dataset
        training: bool = True,
        **kwargs
    ):
        self._root_dir = os.path.join(root_dir, 'dsb2018')
        self._output = output
        self._transforms = transforms
        self._num_calls = num_calls
        self._grayscale = grayscale
        self._grayscale_mode = grayscale_mode
        # specific to this one here
        self.training = training

    def get_image(self, p: Path) -> np.ndarray:
        img = tifffile.imread(p)
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        # img = Image.open(p)
        # img = img.convert(mode='RGB')
        # return np.asarray(img)

    def get_mask(self, p: Path) -> np.ndarray:
        return tifffile.imread(p)
        # if self.training and not isinstance(anno, dict):
        #     # anno: BundlePath
        #     p = anno[0]
        #     val = 1
        #     m0 = imread_asarray(p) > 0
        #     mask = np.zeros_like(m0, dtype=np.uint8)  # uint8 is enough
        #     mask[m0] = val
        #     for p in anno[1:]:
        #         val += 1
        #         m = imread_asarray(p) > 0
        #         # Does not allow overlapping!
        #         mask[m] = val
        #     return mask
        # # anno: dict
        # run_lengths = anno['EncodedPixels']
        # h, w = anno['Height'], anno['Width']
        # mask = rle_decoding_inseg((h, w), run_lengths)
        # return mask

    # @cached_property
    # def ids(self) -> List[str]:
    #     if self.training:
    #         self.root_dir / 'train' /
    #     ids = [line[0] for line in lines]
    #     ids = ordered_unique(ids)
    #     return ids

    @cached_property
    def file_list(self) -> List[Path]:
        # Call MaskDataset.root_dir
        parent = 'train' if self.training else 'test'
        return sorted((self.root_dir / parent / 'images').glob('*.tif'))

    @cached_property
    def anno_dict(self) -> Dict[int, Path]:
        return dict((i, p.parent.with_name('masks') / p.name)
                    for i, p in enumerate(self.file_list))
        # if self.training:
        #     anno_dict = {}
        #     for i, p in enumerate(self.file_list):
        #         anno_dict[i] = list(p.parents[1].glob('masks/*.png'))
        #     return anno_dict
        # else:
        #     anno_rle = {}
        #     _, lines = read_csv(self.root_dir / 'stage1_solution.csv')
        #     # header: ImageId,EncodedPixels,Height,Width,Usage
        #     # iter_rle = map(lambda line: [int(s) for s in line[1].split(' ')],
        #     #                lines)
        #     offset = 0
        #     for i, idx in enumerate(self.ids):
        #         solution: dict = {'EncodedPixels': []}
        #         for line in lines[offset:]:
        #             if idx == line[0]:
        #                 if 'Height' not in solution:
        #                     solution['Height'] = int(line[2])
        #                     solution['Width'] = int(line[3])
        #                 solution['EncodedPixels'].append(
        #                     [int(s) for s in line[1].split(' ')]
        #                 )
        #                 offset += 1
        #             else:
        #                 break
        #         anno_rle[i] = solution
        #     return anno_rle
