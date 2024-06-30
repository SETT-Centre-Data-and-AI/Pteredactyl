# read version from installed package
from importlib.metadata import version

__version__ = version("pteredactyl")

import warnings

import torch

from pteredactyl.defaults import (  # noqa: F401
    DEFAULT_ENTITIES,
    DEFAULT_NER_MODEL,
    DEFAULT_REGEX_ENTITIES,
    DEFAULT_SPACY_MODEL,
    show_defaults,
)
from pteredactyl.redactor import (  # noqa: F401
    analyse,
    anonymise,
    anonymise_df,
    create_analyser,
)
from pteredactyl.regex_entities import build_pteredactyl_recogniser  # noqa: F401

if not torch.cuda.is_available():
    warnings.warn(
        """
CUDA is not installed, so pteredactyl will use CPU rather than GPU.
    -> You can install CUDA 12.1 by running: pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade
    -> Alternatively to select a compatible version visit: https://pytorch.org/get-started/locally/ and generate a pip3 installation command"""
    )
