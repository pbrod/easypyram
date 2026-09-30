"""Tests for PyRAM."""

from pathlib import Path

import numpy as np
import pytest

from easypyram.PyRAM import PyRAM

from easypyram.PyRAMmp import PyRAMArgs


@pytest.fixture
def pyram_args() -> PyRAMArgs:
    """Return common PyRAM constructor arguments."""
    return {
        "freq": 50.0,
        "zs": 50.0,
        "zr": 50.0,
        "z_ss": np.array([0.0, 100.0, 400.0]),
        "rp_ss": np.array([0.0, 25_000.0]),
        "cw": np.array(
            [
                [1480.0, 1530.0],
                [1520.0, 1530.0],
                [1530.0, 1530.0],
            ]
        ),
        "z_sb": np.array([0.0]),
        "rp_sb": np.array([0.0]),
        "cb": np.array([[1700.0]]),
        "rhob": np.array([[1.5]]),
        "attn": np.array([[0.5]]),
        "rbzb": np.array(
            [
                [0.0, 200.0],
                [40_000.0, 400.0],
            ]
        ),
    }


def test_pyram(pyram_args: PyRAMArgs) -> None:
    """Verify PyRAM reproduces the reference RAM solution."""

    dat = np.fromfile(
        Path(__file__).parent / "tl_ref.line",
        sep="\t",
    ).reshape(100, 2)

    ref_r = dat[:, 0]
    ref_tl = dat[:, 1]

    model = PyRAM(rmax=50000, dr=500, dz=2, zmplt=500, c0=1600, **pyram_args)

    model.run()

    np.testing.assert_array_equal(ref_r, model.vr)

    mean_diff = np.mean(np.abs(model.tll - ref_tl))
    assert mean_diff <= 1e-2, f"Mean TL difference ({mean_diff:.6f} dB) exceeds tolerance (0.01 dB)"


def test_default_grid(pyram_args: PyRAMArgs) -> None:
    """Verify the default EasyPyRAM grid spacing."""

    freq = pyram_args["freq"]
    model = PyRAM(**pyram_args)

    wavelength = model._c0 / freq

    assert model._dr == pytest.approx(0.5 * wavelength)
    assert model._dz == pytest.approx(0.05 * wavelength)


def test_pyram_grid(pyram_args: PyRAMArgs) -> None:
    """Verify the original PyRAM grid-spacing preset."""

    freq = pyram_args["freq"]
    model = PyRAM(grid="pyram", **pyram_args)

    pyram_wavelength = 1500.0 / freq

    assert model._dr == pytest.approx(model._np * pyram_wavelength)
    assert model._dz == pytest.approx(0.1 * pyram_wavelength)


def test_grid_partial_override(pyram_args: PyRAMArgs) -> None:
    """Verify an explicit grid step overrides only the corresponding preset value."""
    freq = pyram_args["freq"]
    model = PyRAM(
        grid="pyram",
        dr=20.0,
        **pyram_args,
    )

    pyram_wavelength = 1500.0 / freq

    assert model._dr == pytest.approx(20.0)
    assert model._dz == pytest.approx(0.1 * pyram_wavelength)


def test_grid_partial_dz_override(pyram_args: PyRAMArgs) -> None:
    """Verify explicit dz preserves the preset range step."""
    freq = pyram_args["freq"]

    model = PyRAM(
        grid="pyram",
        dz=2.0,
        **pyram_args,
    )

    wavelength = 1500.0 / freq

    assert model._dr == pytest.approx(model._np * wavelength)
    assert model._dz == pytest.approx(2.0)


def test_invalid_grid(pyram_args: PyRAMArgs) -> None:
    """Verify invalid grid presets are rejected."""

    with pytest.raises(ValueError, match="grid must be 'default' or 'pyram'"):
        PyRAM(
            grid="invalid",
            **pyram_args,
        )

def test_grid_requires_string(pyram_args: PyRAMArgs) -> None:
    """Verify grid preset names must be strings."""
    with pytest.raises(TypeError, match="grid must be a string"):
        PyRAM(
            grid=1,
            **pyram_args,
        )


@pytest.mark.parametrize("grid", ["default", "pyram"])
def test_grid_explicit_dr_dz_override(
    pyram_args: PyRAMArgs,
    grid: str,
) -> None:
    """Verify explicit dr and dz override the selected grid preset."""
    model = PyRAM(
        dr=20.0,
        dz=2.0,
        grid=grid,
        **pyram_args,
    )

    assert model._dr == pytest.approx(20.0)
    assert model._dz == pytest.approx(2.0)


@pytest.mark.parametrize("np_", [4, 8, 12])
def test_pyram_grid_depends_on_pade_terms(
    pyram_args: PyRAMArgs,
    np_: int,
) -> None:
    """Verify the PyRAM range step depends on the number of Padé terms."""
    freq = pyram_args["freq"]

    model = PyRAM(
        grid="pyram",
        np=np_,
        **pyram_args,
    )

    pyram_wavelength = 1500.0 / freq

    assert model._dr == pytest.approx(np_ * pyram_wavelength)
    assert model._dz == pytest.approx(0.1 * pyram_wavelength)
