# SPDX-FileCopyrightText: 2023-present Hanjin Liu <liuhanjin-sc@g.ecc.u-tokyo.ac.jp>
#
# SPDX-License-Identifier: BSD 3-Clause
__version__ = "0.0.1"

from .components.dataframe import MultiIndexDataFrame as DataFrame
from ._io import read_csv

__all__ = ["DataFrame", "read_csv"]
