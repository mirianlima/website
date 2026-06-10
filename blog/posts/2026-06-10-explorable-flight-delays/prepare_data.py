# /// script
# requires-python = ">=3.13"
# dependencies = ["polars", "numpy"]
# ///
"""Generate the synthetic flight-delays dataset for the explorable post.

Run from anywhere: `uv run blog/posts/2026-06-10-explorable-flight-delays/prepare_data.py`
Writes data.parquet next to this script.
"""

from pathlib import Path

import numpy as np
import polars as pl

N_ROWS = 200_000
SEED = 42


def make_flights(n_rows: int = N_ROWS, seed: int = SEED) -> pl.DataFrame:
    """Synthetic flights: arrival delay (min), distance (mi), departure hour."""
    rng = np.random.default_rng(seed)
    return pl.DataFrame(
        {
            "delay": np.clip(rng.gamma(2.0, 15.0, n_rows) - 20, -60, 180).round(0),
            "distance": np.clip(rng.lognormal(6.2, 0.8, n_rows), 80, 3_000).round(0),
            "time": (rng.beta(3.0, 2.0, n_rows) * 24).round(2),
        }
    )


def main() -> None:
    out = Path(__file__).parent / "data.parquet"
    make_flights().write_parquet(out, compression="zstd")
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
