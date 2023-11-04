from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Literal, TypeVar
import polars as pl

from polars_mindex.components.mindex import MultiIndex
from polars_mindex.components import _levels as _lv

if TYPE_CHECKING:
    from polars.type_aliases import NullStrategy

_L = TypeVar("_L", bound=_lv._Levels)

class MultiIndexDataFrame(Generic[_L]):
    def __init__(
        self,
        df: pl.DataFrame,
        index: MultiIndex,
        columns: MultiIndex[_L],
    ):
        self._df = df
        self._index = index
        self._columns = columns
    
    def __getitem__(self, key):
        if isinstance(key, str):
            df_new = self._df.select(self._columns.columns_for_name(key))
            columns_new = self._columns.move_by_key(key)
        elif isinstance(key, tuple):
            # df["name1", "name2"] -> move 2 levels down
            df_new = self._df.select(self._columns.columns_for_names(key))
            columns_new = self._columns.move_by_keys(key)
        else:
            raise TypeError(f"Cannot index MultiIndexDataFrame by {type(key)}")
        if len(columns_new) == 0:
            # NOTE: if key contains slice(None), this never happens
            alias = key if isinstance(key, str) else key[-1]
            return df_new.to_series().alias(alias)
        df_new = df_new.rename(
            {c: ".".join(row) for c, row in zip(df_new.columns, columns_new._df.iter_rows())}
        )
        return MultiIndexDataFrame(df_new, self.index, columns_new)

    def __repr__(self) -> str:
        df = self._df
        df_renamed = df.rename(
            {main: "\n".join(col) + "\n" for col, main in zip(self._columns, df.columns)}
        )
        col_depth = self._columns.nlevels
        index_renamed = self._index._df.rename(
            {c: (" " * len(c) + "\n") * col_depth + c for c in self._index.names}
        )
        return "[multi-indexed] " + repr(pl.concat([index_renamed, df_renamed], how="horizontal"))
    
    @property
    def df(self) -> pl.DataFrame:
        """The polars dataframe behind this object."""
        return self._df
    
    @property
    def index(self) -> MultiIndex:
        """The hierarchical index."""
        return self._index
        
    @property
    def columns(self) -> MultiIndex:
        """The hierarchical columns."""
        return self._columns
    
    def reset_index(self) -> pl.DataFrame:
        """Reset the index to a regular index."""
        return pl.concat([self._index._df, self._df], how="horizontal")

    @property
    def shape(self) -> tuple[int, int]:
        """The shape of the dataframe."""
        return self._df.shape

    def mean(
        self,
        axis: Literal[0, 1] = 0,
        null_strategy: NullStrategy = "ignore",
    ) -> MultiIndexDataFrame[_L]:
        if axis == 0:
            return MultiIndexDataFrame(
                self._df.mean(axis=0, null_strategy=null_strategy), 
                self._columns,
            )
        elif axis == 1:
            return self._df.mean(axis=1, null_strategy=null_strategy)
        else:
            raise ValueError(f"axis must be 0 or 1, got {axis!r}")

    def std(
        self,
        ddof: int = 1,
    ) -> MultiIndexDataFrame[_L]:
        return MultiIndexDataFrame(self._df.std(ddof=ddof), self._columns)
    
    
