#!/bin/bash
#SBATCH --job-name=python   # Job name
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks=1              # Number of tasks
#SBATCH --cpus-per-task=20
#SBATCH --hint=multithread
#SBATCH --time=02:00:00         # Time limit
#SBATCH --partition=shared      # Partition name
#SBATCH --account=phy240043   # Account name
#SBATCH --output=/anvil/scratch/x-ctirapongpra/jobout/%x_%A_%a.out  # Output file for each array task
#SBATCH --error=/anvil/scratch/x-ctirapongpra/jobout/%x_%A_%a.out   # Error file for each array task

module load anaconda
conda activate bayeswave-cpp

# Command to run for each lhid
cd /anvil/scratch/x-ctirapongpra/bayeswave-cpp

export OMP_NUM_THREADS=20

# Job create_data.00000
/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/create_data --ifo H1 --ifo L1 --H1-cache /home/x-ctirapongpra/scratch/gw-collapsar/H1.cache --L1-cache /home/x-ctirapongpra/scratch/gw-collapsar/L1.cache --H1-channel H1:GW-H --L1-channel L1:GW-L --H1-psd /home/x-ctirapongpra/scratch/gw-collapsar/H1_psd.dat --L1-psd /home/x-ctirapongpra/scratch/gw-collapsar/L1_psd.dat --H1-flow 20.0 --L1-flow 20.0 --H1-fhigh 1024.0 --L1-fhigh 1024.0 --srate 4096.0 --seglen 4.0 --dataseed 1272 --trigtime 1126259462 --dont-dump-extras  --overwrite  --gw-wavelets  --waveletDmin 1 --waveletDmax 20 --waveletSNRmin 5 --waveletSNRmax 100 --printWaveforms  --segment-start 1126259460.0 --psdlength 4.0 --psdstart 1126259460.0 --data-directory /home/x-ctirapongpra/scratch/gw-collapsar/two_detectors_output/cached_data_0

# Job bayeswave.00000
/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/main --gw-wavelets  --waveletDmin 1 --waveletDmax 20 --waveletSNRmin 5 --waveletSNRmax 100 --printWaveforms  --Niter 1000000 --Nchain 20 --Nthread 20 --checkpoint  --data-directory /home/x-ctirapongpra/scratch/gw-collapsar/two_detectors_output/cached_data_0 --outputDir /home/x-ctirapongpra/scratch/gw-collapsar/two_detectors_output/bayeswave_output_0
