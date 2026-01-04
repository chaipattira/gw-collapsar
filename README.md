# gw-collapsar

## TO-DO


## Progress Log
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


## brain dump

change --waveletDmax might help

```
REF_VALUES = {
    'antenna_patterns': {
        'H1': (0.578742411175002, -0.45094782109531206),
        'L1': (-0.5274334329518102, 0.20520960891727422)
    },
    't0': {
        'H1': 1126259462.423,
        'L1': 1126259462.4160156
    }
}
```


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
bayeswave-cpp-pipe --config_file /home/x-ctirapongpra/scratch/bayeswave-cpp/bayeswave_cpp_pipe/config.ini --output_directory /home/x-ctirapongpra/scratch/gw-collapsar/two_detectors_output
```

- [x] Debug by opening the file and run the command line by line.

Suspect that the error arises bc it tries to get data from the clusters, so Max suggested we host the data locally.