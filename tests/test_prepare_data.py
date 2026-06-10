"""Tests for the flight-delays dataset generator."""

import importlib.util
from pathlib import Path

SCRIPT = (
    Path(__file__).parent.parent
    / "blog/posts/2026-06-10-explorable-flight-delays/prepare_data.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("prepare_data", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_make_flights_schema_rows_and_bounds():
    mod = load_module()
    df = mod.make_flights(n_rows=1_000, seed=0)
    assert df.columns == ["delay", "distance", "time"]
    assert df.height == 1_000
    assert df["delay"].min() >= -60
    assert df["delay"].max() <= 180
    assert df["distance"].min() >= 80
    assert df["distance"].max() <= 3_000
    assert df["time"].min() >= 0
    assert df["time"].max() < 24


def test_delay_distribution_reaches_into_clip_range():
    mod = load_module()
    df = mod.make_flights(n_rows=200_000, seed=42)
    # Both clip bounds must be genuinely active for the full dataset:
    # early arrivals pile up at -60, extreme delays at 180.
    assert df["delay"].min() == -60
    assert df["delay"].max() == 180


def test_make_flights_is_deterministic():
    mod = load_module()
    a = mod.make_flights(n_rows=100, seed=7)
    b = mod.make_flights(n_rows=100, seed=7)
    assert a.equals(b)
