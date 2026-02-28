#!/bin/bash
#SBATCH --job-name=bw-post
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --hint=multithread
#SBATCH --time=02:00:00
#SBATCH --partition=shared
#SBATCH --account=phy240043
#SBATCH --array=0-11
#SBATCH --output=/anvil/scratch/x-ctirapongpra/jobout/%x_%A_%a.out
#SBATCH --error=/anvil/scratch/x-ctirapongpra/jobout/%x_%A_%a.out

cd /home/x-ctirapongpra/scratch/
module load anaconda
conda activate bayeswave-cpp-postprocessing

export LD_LIBRARY_PATH=/home/x-ctirapongpra/scratch/.conda/envs/2024.02-py311/bayeswave-cpp-postprocessing/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=/home/x-ctirapongpra/scratch/.conda/envs/2024.02-py311/bayeswave-cpp-postprocessing/lib:$DYLD_LIBRARY_PATH

# Array of Frames directories
DIRS=(
    "dur_04s_amp_0.31"
    "dur_04s_amp_0.62"
    "dur_04s_amp_1.25"
    "dur_08s_amp_0.31"
    "dur_08s_amp_0.62"
    "dur_08s_amp_1.25"
    "dur_16s_amp_0.31"
    "dur_16s_amp_0.62"
    "dur_16s_amp_1.25"
    "dur_32s_amp_0.31"
    "dur_32s_amp_0.62"
    "dur_32s_amp_1.25"
)
# Select directory based on array task ID
DIR=${DIRS[$SLURM_ARRAY_TASK_ID]}

echo "Processing ${DIR}"
bayeswave-cpp-post --run_directory /home/x-ctirapongpra/scratch/gw-collapsar/Frames_1000/${DIR}/bayeswave_output_0 --N_waveform_draws all --burn_in half --chain_index 0
# bayeswave-cpp-post --run_directory /home/x-ctirapongpra/scratch/gw-collapsar/Frames/dur_04s_amp_1.25/bayeswave_output_0 --recompute --N_waveform_draws 100 --burn_in half --chain_index 0