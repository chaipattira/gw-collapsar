# gw-collapsar

## Source Parameters

We use gravitational waveforms from collapsar simulations described in [Gottlieb & Lalakos (2024), arXiv:2406.19452](https://arxiv.org/abs/2406.19452).

### Physical Parameters
- **Black hole mass**: MBH = 10 M☉
- **Peak GW frequency**: ~100 Hz
- **Waveform model**: Fiducial collapsar model (Model C) with strongly-cooled accretion disk

### Simulation Configurations

The raw waveform amplitude has been scaled to represent sources at different distances. Since GW amplitude scales as $h ∝ \frac{1}{D}$, the amplitude factors correspond to the following source distances

| Amplitude Factor | Peak Strain (H1/L1) | Luminosity Distance |
|-----------------|---------------------|---------------------|
| 1.25 | ~2.5 × 10⁻²¹ | 8.0 Mpc (Local universe) |
| 0.62 | ~1.2 × 10⁻²¹ | 16.1 Mpc (Virgo cluster distance) |
| 0.31 | ~6.2 × 10⁻²² | 32.3 Mpc (Extended nearby universe) |

### Detector Configuration
Antenna pattern factors and arrival times for LIGO Hanford (H1) and LIGO Livingston (L1) (taken from Max's)
```python
REF_VALUES = {
    'antenna_patterns': {
        'H1': (F_plus=0.578742411175002, F_cross=-0.45094782109531206),
        'L1': (F_plus=-0.5274334329518102, F_cross=0.20520960891727422)
    },
    't0': {
        'H1': 1126259462.423,
        'L1': 1126259462.4160156
    }
}
```

## Progress
- [x] Fixed `Positive<double>` crash in BayesWave for `dur_16s` and `dur_32s` segments (3/3)
  - **Root cause**: input PSD files (`H1_psd.dat`, `L1_psd.dat`) only covered up to 1023.875 Hz, but `create_data` stores the PSD for all frequency bins up to Nyquist (1024 Hz). For 16s segments (0.0625 Hz resolution) and 32s segments (0.03125 Hz resolution), bins above 1023.875 Hz were extrapolated as `inf`, causing a `Positive<double>` assertion failure at runtime.
  - Extended both PSD files from 1023.875 Hz to 1024.0 Hz via linear extrapolation (8032 → 8033 rows each)
  - Changed `fhigh` from 1024.0 Hz to 1023.75 Hz in all 24 `config.ini` files (Frames_100 + Frames_400) — keeps analysis within valid PSD support
  - Changed `waveletDmax` from 400 to 100 in all Frames_400 configs (Frames_100 was already 100)
  - Deleted stale `cached_data_0` for `dur_16s` and `dur_32s` in Frames_400 so they regenerate with the fixed PSD
  - Fixed `run_bayeswave.job` path: was pointing to `Frames_400`, corrected to `Frames_100`
- [x] Fixed Tukey windowing to use fixed 0.5s taper duration per LIGO paper (arxiv:1908.11170) (2/28)
  - Changed from fixed `alpha=0.5` to dynamically calculated alpha based on signal length
  - Ensures exactly 0.5s transition regions on each edge, regardless of signal duration
- [x] Fixed taper order: now applied BEFORE zero-padding (was incorrectly applied after, tapering zeros)
  - Eliminates 1/f spectral leakage from boxcar convolution (see Fig 4 in LIGO paper)
- [x] compute true SNR
- [x] minus 4 on trigger time
- [x] fix postprocess
- [x] plot likelihoods (2/1)
- [x] Increase number of wavelets and change checkpoint time to 8 hrs (1/24)
- [x] Created `plot_experiments.ipynb` to visualize BayesWave reconstruction across all experiments...real strain vs BayesWave reconstruction for 12 experiments (4 lengths × 3 amplitudes) (1/4)
- [x] XLAL frame read error
  - [x] aligned GPS times to start frames at integer GPS times instead of fractional times (1/4)
- [x] Fixed trigtime calculation in `generate_frame_configs.py`: changed `segment_start + 2` to `segment_start + seglen` so `create_data` reads the correct time window (1/4)
- [x] Rewrote `run_bayeswave.job` to parallelize jobs (1/4)
- [x] Created `build_all.sh` script to run bayeswave-cpp-pipe for all 9 Frame configurations (1/4)
- [x] config.ini files for 9 frames with appropriate seglen, cache-dict, psd-dict, and trigtime (1/4)
- [x] Created `preprocess_batch.ipynb` to generate 9 frame configurations (3 durations × 3 amplitudes) for BayesWave testing (1/4)
  - [x] Fixed asymmetric crop bug in `preprocess_batch.ipynb` that caused 32s duration PSDs to be all zeros (1/4)
- [x] Took care of the lurking technical debts and rewrote all the code to fix all the minor bugs. Now have very streamlined preprocessing notebook (1/3).
- [x] Fix some BayesWave dependencies (12/31)
- [x] Run the thing (12/9)
    - it actually works! By eye inspection, Bayeswave appears to be capable of reconstructing the signal. There appears to be a time mismatch between what Bayeswave outputs and my frame file, so I recalibrated accordingly.
- [x] fix multithreading with ``export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK``
- [x] Load signal and reproduce plots of h(t) vs. t (should correlate with figure 3)
- [x] use gwpy to create time series class and save it as .gwf file (Frame file)
- [x] We want to do source reconstruction so we replace --glitch with --gw_wavelets and include --printWaveforms in the config.
- [x] Try to gen plots for GW150914 and simulated data of GW150914 from local disk (10/23)
- [x] Run BayesWaveCpp Pipe for the example. This package will setup the directory for you (quite convenient). Don't forget to change the directory in the config file. Make sure that it runs and produces that nice webpage with the stats.
	- [x] Wait for Max's PSD file (10/8)
	- [x] Need LIGO username (10/23)
      - No, you don't!
- [x] Run the GW example again with a bunch of CPUs and push the result to Github


## Notes

- Increasing `--waveletDmax` may improve reconstruction quality for long-duration signals
- Consider adjusting prior on trigger time and increasing burn-in for better convergence

## Admin stuff
-  Installing (DON'T FORGET TO USE THE NEW ``environment.yaml``)
```bash
# first time
git clone https://git.ligo.org/bayeswave/bayeswave-cpp.git

# activate conda
source ~/.bashrc 

# create new environment
conda env create --file /home/x-ctirapongpra/scratch/bayeswave-cpp/environment.yaml -y

python -m pip install gwpy lalsuite
python -m ipykernel install --user --name=bayeswave-cpp --display-name "bayeswave-cpp"

# For gw processing or else floating point error
conda install -c conda-forge python-ldas-tools-framecpp
conda install -c conda-forge python-framel
```

- Building and install python bindings
```bash
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build -j5
cd build
ctest --output-on-failure
cd ..

pip install -e .
```

- Run
```
bayeswave-cpp-pipe --config_file /home/x-ctirapongpra/scratch/gw-collapsar/Frames/dur_08s_amp_2.50/config.ini --output_directory /home/x-ctirapongpra/scratch/gw-collapsar/two_detectors_output
```

- [x] Debug by opening the file and run the command line by line.

Suspect that the error arises bc it tries to get data from the clusters, so Max suggested we host the data locally.


prior on the time
increase burnin
single sine gaussian