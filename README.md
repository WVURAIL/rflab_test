# rflab_test

> Archived 20 August 2026. This is a read-only historical collection; no
> hardware support or ongoing maintenance is provided.

Python scripts for RF laboratory instruments and measurements from the WVU
Radio Astronomy Instrumentation Lab, committed to this repository from 2019
through 2021.

## Keysight network analyser scripts

The dedicated
[`keysight_network_analyser_control`](https://github.com/WVURAIL/keysight_network_analyser_control)
repository is the canonical archive for the Keysight VNA scripts.

The scripts and licence under `keysight_na/` are a frozen 2021 snapshot retained
for old links and provenance; its README adds archival context above the
original instructions. The snapshot was copied from the dedicated repository
rather than split from this repository, so the two Git histories remain
separate. New use should start from the dedicated archive.

## Contents

### `rflab_scripts/`

Measurement and plotting tools built around lab instruments.

| Script | Purpose |
|---|---|
| `noise_figure.py` | Noise-figure measurement and processing |
| `hp8970a.py` | HP 8970A noise-figure meter control |
| `smith.py` | Smith-chart plotting |
| `stability.py`, `stab_factor_rev3.py` | Amplifier stability factors |
| `logmag.py` | Log-magnitude plots from S-parameter data |
| `plot_s2p.py` | Quick plotting of a Touchstone `.s2p` file |
| `make_all_plots.py` | Batch plotting across a measurement set |
| `antpy.py` | Antenna-measurement helpers |
| `RSA306B_example_python_access_windows.py` | Tektronix RSA306B access |

### `legacy/`

Older VNA and spectrum-analyser transfer scripts. They are retained because
they cover instruments and transfer paths not represented by the newer files.

## Compatibility

These scripts have not been tested with the original instruments during the
archive review. Of the 21 Python files outside `keysight_na/`, 13 compile under
Python 3 and these 8 do not:

- `rflab_scripts/noise_figure.py`
- `rflab_scripts/smith.py`
- `rflab_scripts/logmag.py`
- `rflab_scripts/antpy.py`
- `rflab_scripts/hp8970a.py`
- `rflab_scripts/RSA306B_example_python_access_windows.py`
- `legacy/RSA_CSV_Processor.py`
- `legacy/vna_control.py`

Most use Python 2 syntax. `legacy/vna_control.py` also contains 298 non-breaking
spaces used in indentation; replacing them mechanically would change its block
structure. The files were left unchanged because a reliable port requires the
original hardware and data. Files named `test.py` or `test_make_all_plots.py`
are manual drivers, not an automated test suite.

Dependencies were not pinned. Imports across the collection include NumPy,
Matplotlib, SciPy, scikit-rf, and PyVISA; instrument control also requires a
compatible VISA implementation.

## Preservation notes

- All original commits through
  [`f3f709d`](https://github.com/WVURAIL/rflab_test/commit/f3f709dc623582bcd3f91bb5ad2701c3f978085a)
  remain unchanged and reachable.
- The former `Framework` branch contained no commits outside `master`.
- A short-lived 2021 commit recorded `rflab` as a Git link without a
  `.gitmodules` file. The referenced nested commit,
  `4e7b6664cbf8323899021038dd0f8de7060d2d98`, could not be recovered, but the
  13-file snapshot that replaced it four minutes later is preserved in
  `rflab_scripts/`.
- The pre-archive rflab history records work by Pranav Sanghavi and Jacob
  Hanni. Kevin Bandura is named in `rflab_scripts/contributors.txt`. The
  dedicated Keysight repository's history records work by Pranav Sanghavi and
  Joseph Shepard.

See [`NOTICE.md`](NOTICE.md) for rights information.
