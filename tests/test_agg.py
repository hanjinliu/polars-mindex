import polars as pl

from polars_mindex import agg
from functools import cache

@cache
def _get_df(ncat=1):
    df = pl.DataFrame(
        {"cat0": ["a", "b", "a", "b", "a", "b", "a", "b"],
         "cat1": [0, 0, 0, 0, 0, 1, 1, 1],
         "val0": [1, 2, 3, 4, 5, 6, 7, 8],
         "val1": [5, 6, 7, 8, 9, 10, 11, 12],
         }
    )
    
    if ncat == 2:
        grouped = df.group_by("cat0", "cat1")
        return agg(grouped, ["mean", "std"])
    elif ncat == 1:
        grouped = df.drop("cat1").group_by("cat0")
        return agg(grouped, ["mean", "std"])
    raise RuntimeError

def test_agg_works():
    dfm = _get_df()
    assert dfm.shape == (2, 4)
    
def test_getitem_columns_and_levels():
    dfm = _get_df(2)
    assert dfm.index.nlevels == 2
    assert dfm.index.names == ["cat0", "cat1"]
    assert set(dfm.index.values(0)) == {"a", "b"}
    assert dfm.columns.nlevels == 2
    assert dfm.columns.values(0) == ["val0", "val0", "val1", "val1"]
    assert dfm.columns.values(1) == ["mean", "std", "mean", "std"]
    
    df0 = dfm["val0"]
    assert df0.columns.nlevels == 1
    assert df0.columns.values(0) == ["mean", "std"]
    assert isinstance(df0["mean"], pl.Series)
    assert df0["mean"].name == "mean"
    
    assert isinstance(dfm["val0", "mean"], pl.Series)
    assert dfm["val0", "mean"].name == "mean"