# EasyPyRAM

**EasyPyRAM** is a user-friendly Python implementation of the
Range-dependent Acoustic Model (RAM) for underwater acoustic propagation.

The project builds on PyRAM while placing additional emphasis on ease of use,
sensible defaults, structured results, documentation, examples, testing, and
modern Python development practices.

EasyPyRAM aims to lower the barrier to using RAM without hiding the numerical
parameters that experienced users may need to control.

## Background

RAM was created by Michael D. Collins at the U.S. Naval Research Laboratory.
The Python implementation is based on RAM v1.5, available from the
Ocean Acoustics Library:

https://oalib-acoustics.org/models-and-software/parabolic-equation

PyRAM was developed by Marcus Donnelly to provide a version of RAM that can be
used directly within a Python environment, such as IPython, Spyder, or Jupyter,
and that is easier to understand, extend, and integrate into other applications
than the original Fortran implementation.

The implementation is written in Python and uses Numba JIT compilation for the
computationally intensive numerical routines, providing performance comparable
to compiled native code while retaining a Python interface.

The `PyRAM` class largely follows the structure of the original RAM Fortran
implementation. Many methods correspond directly to the original Fortran
subroutines and functions and retain similar names and variable conventions.
Some Fortran routines that are unnecessary in Python have been replaced by
functionality provided by NumPy and other standard scientific Python tools.

As in PyRAM, sound-speed profile updates with range are decoupled from seabed
parameter updates. This provides greater flexibility when environmental data
come from different sources or have different horizontal sampling intervals.

## Why EasyPyRAM?

EasyPyRAM retains the RAM numerical model and the core design of PyRAM while
providing a more accessible interface for both new and experienced users.

In particular, EasyPyRAM provides:

- sensible default numerical parameters that allow users to get started
  without first having to tune the RAM computational grid;
- structured, typed results with convenient access to transmission loss,
  complex pressure, ranges, depths, and model metadata;
- built-in sound-speed profile helpers, including Munk and idealized Arctic
  profiles;
- practical examples demonstrating typical underwater-acoustic propagation
  problems;
- expanded documentation covering model configuration, numerical accuracy,
  stability, and parameter selection;
- NumPy-based inputs and outputs for straightforward integration with the
  scientific Python ecosystem;
- multiprocessing support for running multiple frequencies or acoustic
  environments in parallel;
- modern Python packaging, testing, static type checking, and continuous
  integration.

The default range and depth steps are automatically selected from the acoustic
wavelength, providing a practical starting point for new users. Experienced
users can override these and the other numerical parameters when finer control
is required.

## Installation

EasyPyRAM requires Python 3.10 or later.

Install the latest release from PyPI:

```bash
python -m pip install easypyram
```

To include the optional plotting dependencies used by the examples:

```bash
python -m pip install "easypyram[plot]"
```

To install the latest development version directly from GitHub:

```bash
python -m pip install "git+https://github.com/pbrod/easypyram.git"
```

## Quick Start

The following example calculates transmission loss for a simple
range-independent environment:

```python
import numpy as np

from easypyram import PyRAM

pyram = PyRAM(
    freq=50.0,
    zs=50.0,
    zr=50.0,
    z_ss=np.array([0.0, 100.0, 400.0]),
    rp_ss=np.array([0.0]),
    cw=np.array(
        [
            [1480.0],
            [1520.0],
            [1530.0],
        ]
    ),
    z_sb=np.array([0.0]),
    rp_sb=np.array([0.0]),
    cb=np.array([[1700.0]]),
    rhob=np.array([[1.5]]),
    attn=np.array([[0.5]]),
    rbzb=np.array(
        [
            [0.0, 400.0],
            [50_000.0, 400.0],
        ]
    ),
    rmax=50_000.0,
)

result = pyram.run()
```

EasyPyRAM returns a structured `PyRAMResults` object. Model outputs are
therefore directly available as attributes:

```python
result.ranges
result.depths

result.loss_line
result.loss_grid

result.pressure_line
result.pressure_grid

result.c0
result.proc_time
```

For example, transmission loss at the receiver depth can be plotted with:

```python
import matplotlib.pyplot as plt

plt.plot(result.ranges / 1000.0, result.loss_line)
plt.xlabel("Range [km]")
plt.ylabel("Transmission loss [dB]")
plt.grid()
plt.show()
```

## Sound-Speed Profiles

EasyPyRAM provides helpers for constructing representative sound-speed
profiles.

### Munk profile

The canonical Munk deep-ocean sound-speed profile can be evaluated at arbitrary
depths:

```python
import numpy as np

from easypyram import munk_profile

depth = np.arange(0.0, 5000.0, 10.0)
sound_speed = munk_profile(depth)
```

### Arctic profile

An idealized Arctic profile is also provided:

```python
from easypyram import arctic_profile

sound_speed = arctic_profile(depth)
```

The profiles can be compared directly:

```python
import matplotlib.pyplot as plt
import numpy as np

from easypyram import arctic_profile, munk_profile

depth = np.arange(0.0, 2000.0)

plt.plot(munk_profile(depth), depth, label="Munk")
plt.plot(arctic_profile(depth), depth, label="Arctic")

plt.xlabel("Sound speed [m/s]")
plt.ylabel("Depth [m]")
plt.gca().invert_yaxis()
plt.legend()
plt.show()
```

## Relationship to RAM and PyRAM

RAM was developed by Michael D. Collins at the U.S. Naval Research Laboratory.

PyRAM was developed by Marcus Donnelly as a Python adaptation of RAM. 

EasyPyRAM is derived from PyRAM and is independently maintained, with an
emphasis on ease of use, sensible defaults, structured results, documentation,
examples, and modern Python development practices.
 
EasyPyRAM is not an official version of RAM or PyRAM.