# polars-mindex

[![PyPI - Version](https://img.shields.io/pypi/v/polars-mindex.svg)](https://pypi.org/project/polars-mindex)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/polars-mindex.svg)](https://pypi.org/project/polars-mindex)

Use MultiIndex in polars.

-----

**Table of Contents**

- [polars-mindex](#polars-mindex)
  - [What is this for?](#what-is-this-for)
  - [Installation](#installation)
  - [License](#license)

## What is this for?

[`polars`](https://github.com/pola-rs/polars) does not use MultiIndex, but MultiIndex is very useful for data analysis with REPL.

```python
import polars_mindex as plm

df = plm.DataFrame(
    {
        "cat": ["A", "A", "B", "B"],
        "value-0": [0.3, 0.5, 0.2, 0.1],
        "value-1": [2.4, 3.6, 4.8, 1.2],
    }
)

df_agg = df.group_by("cat").agg(["mean", "std"])
df_agg
```

```
[multi-indexed] shape: (2, 5)
┌─────┬─────────┬──────────┬─────────┬──────────┐
│     ┆ value-0 ┆ value-0  ┆ value-1 ┆ value-1  │
│     ┆ mean    ┆ std      ┆ mean    ┆ std      │
│ cat ┆         ┆          ┆         ┆          │
│ --- ┆ ---     ┆ ---      ┆ ---     ┆ ---      │
│ str ┆ f64     ┆ f64      ┆ f64     ┆ f64      │
╞═════╪═════════╪══════════╪═════════╪══════════╡
│ A   ┆ 0.4     ┆ 0.141421 ┆ 3.0     ┆ 0.848528 │
│ B   ┆ 0.15    ┆ 0.070711 ┆ 3.0     ┆ 2.545584 │
└─────┴─────────┴──────────┴─────────┴──────────┘
```

```python
df_agg["value-0"]
```

```
┌─────┬──────┬──────────┐
│     ┆ mean ┆ std      │
│ cat ┆      ┆          │
│ --- ┆ ---  ┆ ---      │
│ str ┆ f64  ┆ f64      │
╞═════╪══════╪══════════╡
│ A   ┆ 0.4  ┆ 0.141421 │
│ B   ┆ 0.15 ┆ 0.070711 │
└─────┴──────┴──────────┘
```


## Installation

```console
pip install polars-mindex
```

## License

`polars-mindex` is distributed under the terms of the [BSD 3-Clause](https://spdx.org/licenses/BSD 3-Clause.html) license.
