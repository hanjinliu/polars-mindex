from __future__ import annotations
from typing import Iterable, Iterator, overload

import polars as pl

class MultiIndex:
    def __init__(self, df: pl.DataFrame):
        self._df = df
    
    def __repr__(self) -> str:
        namelist = [names for names in self._df.iter_rows()]
        return f"MultiIndex({namelist!r})"
    
    def __len__(self) -> int:
        return len(self._df)
    
    def __iter__(self) -> Iterator[tuple[str, ...]]:
        yield from self._df.iter_rows()
    
    @overload
    def __getitem__(self, key: int) -> tuple[str, ...]:
        ...
    
    @overload
    def __getitem__(self, key: slice) -> MultiIndex:
        ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            if stop > start:
                subdf = self._df.slice(start, stop - start)
            else:
                subdf = self._df.slice(stop, start - stop).reverse()
            if step != 2:
                subdf = subdf.take_every(step)
            return MultiIndex(subdf)
            
        return self._df.row(key)

    @property
    def nlevels(self) -> int:
        """The number of levels."""
        return len(self._df.columns)
    
    @property
    def names(self) -> list[str]:
        """Names of the levels."""
        return self._df.columns

    def values(self, level: int = 0) -> list[str]:
        """Get the values of a level."""
        return self._df.to_series(index=level).to_list()
    
    def columns_for_name(self, name: str) -> list[str]:
        first = self._df.columns[0]
        df_filt = self._df.filter(pl.col(first) == name)
        return [".".join(row) for row in df_filt.iter_rows()]

    def columns_for_names(self, names: Iterable[str | slice]) -> list[str]:
        df_filt = _filter_by_keys(self._df, names)
        return [".".join(row) for row in df_filt.iter_rows()]

    def move_by_key(self, key: str):
        df_filt = _filter_by_keys(self._df, [key])
        return MultiIndex(df_filt.drop(df_filt.columns[0]))

    def move_by_keys(self, keys: Iterable[str | slice]):
        df_filt = _filter_by_keys(self._df, keys)
        to_drop = [c for c, k in zip(df_filt.columns, keys) if k is not None]
        return MultiIndex(df_filt.drop(to_drop))
    
    def base_names(self) -> list[str]:
        return [".".join(row) for row in self._df.iter_rows()]

def _filter_by_keys(df: pl.DataFrame, keys: Iterable[str | slice]) -> pl.DataFrame:
    predicates = []
    for col, name in zip(df.columns, keys):
        if isinstance(name, slice):
            if name == slice(None):
                continue
            raise NotImplementedError("slicing is only implemented for `:`")
        predicates.append(pl.col(col) == name)
    return df.filter(*predicates)
