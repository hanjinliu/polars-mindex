from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterable, overload
import polars as pl
from polars_mindex.components.dataframe import MultiIndexDataFrame

from polars_mindex.components.mindex import MultiIndex

if TYPE_CHECKING:
    from polars.dataframe.group_by import GroupBy as _GroupBy
    from polars_mindex.components.types import DataFrame2Lv


AGG_EXPR_FUNCS: dict[str, Callable[[pl.Expr], pl.Expr]] = {
    "mean": lambda e: e.mean(),
    "std": lambda e: e.std(),
    "var": lambda e: e.var(),
    "min": lambda e: e.min(),
    "max": lambda e: e.max(),
    "sum": lambda e: e.sum(),
    "first": lambda e: e.first(),
    "last": lambda e: e.last(),
    "median": lambda e: e.median(),
    "n_unique": lambda e: e.n_unique(),
    "count": lambda e: e.count(),
}


def make_agg(col: str, agg: str) -> pl.Expr:
    return AGG_EXPR_FUNCS[agg](pl.col(col))


class GroupBy:
    def __init__(self, g: _GroupBy):
        self._g = g
        assert g.maintain_order

    @overload
    def agg(self, funcs: str | Iterable[str]) -> DataFrame2Lv:
        ...

    @overload
    def agg(self, *aggs: str) -> DataFrame2Lv:
        ...

    def agg(self, *aggs):
        if len(aggs) == 1 and not isinstance(aggs[0], str):
            aggs = aggs[0]
            if not hasattr(aggs, "__iter__"):
                raise TypeError(f"aggs must be iterable, get {type(aggs)!r}")
        index_df = self._g.df.select(self._g.by, *self._g.more_by).unique(maintain_order=True)
        main_df_cols = [c for c in self._g.df.columns if c not in index_df.columns]
        exprs: list[pl.Expr] = []
        level0 = []
        level1 = []
        for col in main_df_cols:
            for agg in aggs:
                if not isinstance(agg, str):
                    raise TypeError(f"each agg must be str, get {type(agg)!r}")
                exprs.append(make_agg(col, agg).alias(f"{col}.{agg}"))
                level0.append(col)
                level1.append(agg)

        out = self._g.agg(exprs)
        columns = pl.DataFrame({"level_0": level0, "level_1": level1})

        main_df = out.select(c for c in out.columns if c not in index_df.columns)
        return MultiIndexDataFrame(
            main_df,
            MultiIndex(index_df),
            MultiIndex(columns),
        )
