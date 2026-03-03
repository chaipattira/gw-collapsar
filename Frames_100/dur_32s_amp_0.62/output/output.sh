# Job create_data.00000
/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/create_data --ifo H1 --ifo L1 --H1-cache /home/x-ctirapongpra/scratch/gw-collapsar/Frames_100/dur_32s_amp_0.62/H1.cache --L1-cache /home/x-ctirapongpra/scratch/gw-collapsar/Frames_100/dur_32s_amp_0.62/L1.cache --H1-channel H1:GW-H --L1-channel L1:GW-L --H1-psd /home/x-ctirapongpra/scratch/gw-collapsar/PSD/H1_psd.dat --L1-psd /home/x-ctirapongpra/scratch/gw-collapsar/PSD/L1_psd.dat --H1-flow 20.0 --L1-flow 20.0 --H1-fhigh 1024.0 --L1-fhigh 1024.0 --srate 4096.0 --seglen 32.0 --dataseed 1272 --segment-start 1126259446 --trigtime 1126259462.0.0 --psdlength 32.0 --psdstart 1126259446 --dont-dump-extras  --overwrite  --gw-wavelets  --waveletDmin 1 --waveletDmax 100 --waveletSNRmin 5 --waveletSNRmax 200 --printWaveforms  --checkpointingIntervalHrs 24 --data-directory cached_data_0

# Job bayeswave.00000
/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/main --gw-wavelets  --waveletDmin 1 --waveletDmax 100 --waveletSNRmin 5 --waveletSNRmax 200 --printWaveforms  --checkpointingIntervalHrs 24 --Niter 5000000 --Nchain 20 --Nthread 20 --checkpoint  --data-directory cached_data_0 --outputDir bayeswave_output_0

# Job bayeswave_post.00000
/home/x-ctirapongpra/scratch/.conda/envs/2024.02-py311/bayeswave-cpp/bin/bayeswave-cpp-post --recompute  --N_waveform_draws all --burn_in half --run_directory bayeswave_output_0

