from typing import TYPE_CHECKING, overload
import polars as pl
from polars_mindex.components.dataframe import MultiIndexDataFrame
from polars_mindex.components import _levels as _lv

if TYPE_CHECKING:
    class DataFrame1Lv(MultiIndexDataFrame[_lv._1]):
        @overload
        def __getitem__(self, key: str) -> pl.Series:
            ...

    class DataFrame2Lv(MultiIndexDataFrame[_lv._2]):
        @overload
        def __getitem__(self, key: str) -> DataFrame1Lv:
            ...

        @overload
        def __getitem__(self, key: tuple[str, str]) -> pl.Series:
            ...
        
        @overload
        def __getitem__(self, key: tuple[slice, str] | tuple[str, slice]) -> DataFrame1Lv:
            ...

        def __getitem__(self, key):
            return super().__getitem__(key)

    class DataFrame3Lv(MultiIndexDataFrame[_lv._3]):
        @overload
        def __getitem__(self, key: str) -> DataFrame2Lv:
            ...
        
        @overload
        def __getitem__(self, key: tuple[str, str]) -> DataFrame1Lv:
            ...

        @overload
        def __getitem__(self, key: tuple[str, str, str]) -> pl.Series:
            ...

        def __getitem__(self, key):
            return super().__getitem__(key)

    class DataFrame4Lv(MultiIndexDataFrame[_lv._4]):
        @overload
        def __getitem__(self, key: str) -> DataFrame3Lv:
            ...
        
        @overload
        def __getitem__(self, key: tuple[str, str]) -> DataFrame2Lv:
            ...

        @overload
        def __getitem__(self, key: tuple[str, str, str]) -> DataFrame1Lv:
            ...

        @overload
        def __getitem__(self, key: tuple[str, str, str]) -> pl.Series:
            ...

        def __getitem__(self, key):
            return super().__getitem__(key)
