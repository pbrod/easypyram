# Changelog

## [2.1.1] - 2026-09-30

### 📚 Documentation

- *(readme)* Fix repository, changelog, migration, and license links when rendered on PyPI

## [2.1.0] - 2026-09-30

### 🚀 Features

- *(PyRAM)* Add `grid="pyram"` preset for reproducing PyRAM v1.x automatic grid spacing
- *(PyRAM)* Add `grid="default"` preset for EasyPyRAM wavelength-based grid spacing
- *(PyRAM)* Allow explicit `dr` and `dz` values to override grid preset values

### 🧪 Testing

- *(PyRAM)* Add tests for grid presets, explicit overrides, validation, and Padé-term dependence

### 📚 Documentation

- *(readme)* Update README with EasyPyRAM 2.x usage and PyRAM migration guidance
- *(PyRAM)* Document grid presets, numerical recommendations, and PyRAM compatibility behavior

## [2.0.0] - 2026-09-29

### 🚀 Features

- Establish EasyPyRAM as an independently maintained fork of PyRAM with an emphasis on usability
- Add sound-speed profile helper functions for Munk and idealized Arctic profiles
- Add `PyRAMResults` NamedTuple for structured and typed model outputs
- Add four usage examples, including an Arctic and Munk sound-speed profile comparison
- Revise default grid-spacing calculations to provide more robust starting values

### ⚠️ Breaking Changes

- Rename the distribution and Python package from `pyram` to `easypyram`
- Replace dictionary-based output from `PyRAM.run()` with the `PyRAMResults` result object
- Replace dictionary keys and abbreviated result names with descriptive
  attributes such as `loss_grid`, `loss_line`, `pressure_grid`, and
  `pressure_line`
- Change the default calculation steps to `dr = 0.5 * wavelength`
  and `dz = 0.05 * wavelength`


### 🔄 Migration from PyRAM v1.x

EasyPyRAM v2.0.0 introduces breaking API changes compared with PyRAM v1.x.

#### Package imports

The package has been renamed from `pyram` to `easypyram`.

Before:

```python
from pyram import PyRAM
```


After:

```python
from easypyram import PyRAM
```

#### Model results

`PyRAM.run()` now returns a `PyRAMResults` NamedTuple instead of a dictionary.

Before:

```python
result = model.run()

ranges = result["Ranges"]
depths = result["Depths"]
loss_grid = result["TL Grid"]
loss_line = result["TL Line"]
pressure_grid = result["CP Grid"]
pressure_line = result["CP Line"]
c0 = result["c0"]
proc_time = result["Proc Time"]
run_id = result["ID"]
```


After:

```python
result = model.run()

ranges = result.ranges
depths = result.depths
loss_grid = result.loss_grid
loss_line = result.loss_line
pressure_grid = result.pressure_grid
pressure_line = result.pressure_line
c0 = result.c0
proc_time = result.proc_time
run_id = result.id
```

The result fields have the following correspondence:

- `Ranges` → `ranges`
- `Depths` → `depths`
- `TL Grid` → `loss_grid`
- `TL Line` → `loss_line`
- `CP Grid` → `pressure_grid`
- `CP Line` → `pressure_line`
- `c0` → `c0`
- `Proc Time` → `proc_time`
- `ID` → `id`

#### Default numerical parameters

The default range and depth calculation steps have changed to wavelength-based values intended to provide robust starting values:


```python
dr = 0.5 * wavelength
dz = 0.05 * wavelength
```

Applications that need to reproduce results generated with PyRAM v1.x defaults should explicitly specify `dr` and `dz`.


#### Input arrays

EasyPyRAM makes internal copies of user-supplied environmental arrays. Running the model therefore no longer modifies arrays owned by the caller.

#### Multiprocessing

`PyRAMmp` remains available through the EasyPyRAM namespace:

```python
from easypyram import PyRAMmp
```

Results from multiprocessing runs use the same `PyRAMResults` interface as
sequential runs.

#### Installation

EasyPyRAM is distributed separately from PyRAM. Replace the `pyram` dependency
with `easypyram`:

```bash
python -m pip install easypyram
```

Optional plotting support can be installed with:

```bash
python -m pip install "easypyram[plot]"
```


### 🐛 Bug Fixes

- Prevent mutation of user-supplied input arrays
- Fix stale `pyram` imports following the EasyPyRAM package rename
- Save `LICENSE.md` as UTF-8 for cross-platform package builds
- Correct the PDM cache configuration used by GitHub Actions

### ⚙️ Maintenance

- Vectorize the `profl()` method
- Remove obsolete `setup.py`
- Remove legacy and unused PyRAM code
- Remove obsolete `MANIFEST.in`
- Refresh examples and supporting files
- Refresh PDM lock files

### ♻️ Refactoring

- Restructure the project using a `src` package layout
- Rename the source package from `src/pyram` to `src/easypyram`
- Update package imports and references to the `easypyram` namespace
- Move examples into a dedicated `examples.py` module
- Update examples to use the new results API
- Simplify PyRAM and PyRAMmp tests
- Expose `PyRAMResults` through the public API
- Add type hints throughout the codebase

### 📚 Documentation

- Rewrite the README for EasyPyRAM
- Document the relationship and lineage between RAM, PyRAM, and EasyPyRAM
- Add comprehensive RAM documentation and references
- Convert API documentation to NumPy-style docstrings
- Document numerical parameter selection and grid sizing
- Include original RAM documentation (`readme.orig`)
- Add `CHANGELOG.md` with historical PyRAM release notes
- Update BSD license copyright attribution for EasyPyRAM

### 🎨 Styling

- Apply consistent formatting with Ruff

### 📦 Build System

- Modernize packaging and development tooling using `pyproject.toml` and PDM
- Add optional plotting support via Matplotlib
- Add PDM lock files for supported Python versions
- Add separate dependency locking for Python 3.14
- Add release automation and dynamic versioning
- Add git-cliff configuration for changelog generation

### 🏗️ CI/CD

- Add GitHub Actions CI workflow
- Test EasyPyRAM across Linux, Windows, and macOS
- Enable Ruff formatting and linting, MyPy type checking, and pytest validation
- Add dedicated formatting checks
- Optimize testing and package build jobs
- Add CI validation for the `develop` branch
- Add automated PyPI release workflow for version tags
- Verify built wheel installation before release
- Make MyPy checks use the active Python version across the CI matrix
- Remove experimental Python 3.15 RC testing until Numba and llvmlite provide support

## [1.3.0] - 2025-03-28

### 🐛 Bug Fixes

- Replace deprecated `numpy.complex` with `numpy.complex128`.

### ⚙️ Maintenance

- Apply minor code cleanups and maintenance updates.

### 📚 Documentation

- Refresh docstrings and project documentation.
- Update Ocean Acoustics Library (OALIB) URLs.

---

## [1.2.0] - 2019-07-08

### 🚀 Features

- Return complex acoustic pressure fields from model runs.
- Return reference sound speed (`c0`) with model outputs.

### 🐛 Bug Fixes

- Correct handling of range-dependent environments with range intervals smaller than `dr`.
- Fix output grid depth indexing so output values are reported at the correct depths.
- Ensure `outpt()` cannot index beyond output array bounds.
- Correct seabed profile depth handling relative to the deepest water-profile depth.
- Fix `PyRAMmp` so multiple batches of runs are handled correctly.

### ⚙️ Maintenance

- Improve multiprocessing test flexibility with configurable repetitions (`nrep`).
- Correct multiprocessing speed-up calculation.
- Update conda packaging recipe.

### 🚀 Multiprocessing

- Add the `PyRAMmp` multiprocessing interface for parallel model execution.

### 🧪 Testing

- Improve `PyRAMmp` test coverage and validation.

---

## [1.1.7] - 2018-11-10

### 🧪 Testing

- Improve the `PyRAMmp` regression and performance test suite.

### 🐛 Bug Fixes

- Ensure `outpt()` cannot index beyond the end of output arrays.

---

## [1.0.1] - 2017-11-30

### 🐛 Bug Fixes

- Correct handling of `dr`, `ndr`, and `ndz`.
- Fix an issue where `ndr` and `ndz` were not being applied during output generation.

### 🚀 Performance

- Add Numba JIT compilation support.
- JIT-compile the `outpt()` routine.
- Remove unused function `g`.
- Introduce the `run()` method API.

### ♻️ Refactoring

- Perform minor code refactoring and cleanup.
- Apply additional bug fixes and internal restructuring.

### ⚙️ Packaging

- Add conda build recipe.
- Update conda packaging configuration.

### 🔬 Validation

- Regenerate reference transmission loss data using a Fortran build compiled with `-O3`.