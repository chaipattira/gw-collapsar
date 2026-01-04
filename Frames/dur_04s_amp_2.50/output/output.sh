# Job create_data.00000
/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/create_data --ifo H1 --ifo L1 --H1-cache /home/x-ctirapongpra/scratch/gw-collapsar/Frames/dur_04s_amp_2.50/H1.cache --L1-cache /home/x-ctirapongpra/scratch/gw-collapsar/Frames/dur_04s_amp_2.50/L1.cache --H1-channel H1:GW-H --L1-channel L1:GW-L --H1-psd /home/x-ctirapongpra/scratch/gw-collapsar/Frames/dur_04s_amp_2.50/H1_psd.dat --L1-psd /home/x-ctirapongpra/scratch/gw-collapsar/Frames/dur_04s_amp_2.50/L1_psd.dat --H1-flow 20.0 --L1-flow 20.0 --H1-fhigh 1024.0 --L1-fhigh 1024.0 --srate 4096.0 --seglen 4.0 --dataseed 1272 --segment-start 1126259460 --trigtime 1126259464.0 --psdlength 4.0 --psdstart 1126259460 --dont-dump-extras  --overwrite  --gw-wavelets  --waveletDmin 1 --waveletDmax 20 --waveletSNRmin 5 --waveletSNRmax 100 --printWaveforms  --data-directory cached_data_0

# Job bayeswave.00000
/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/main --gw-wavelets  --waveletDmin 1 --waveletDmax 20 --waveletSNRmin 5 --waveletSNRmax 100 --printWaveforms  --Niter 1000000 --Nchain 20 --Nthread 20 --checkpoint  --data-directory cached_data_0 --outputDir bayeswave_output_0

