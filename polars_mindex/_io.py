from __future__ import annotations

from functools import wraps
import polars as pl
from polars_mindex.components.dataframe import MultiIndexDataFrame


@wraps(pl.read_csv)
def read_csv(*args, **kwargs):
    df = pl.read_csv(*args, **kwargs)
    return MultiIndexDataFrame(df)
