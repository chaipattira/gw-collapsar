#!/bin/bash
# Run bayeswave-cpp-pipe for every subfolder in three_detectors that has a config.ini

FRAMES_BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd /anvil/scratch/x-ctirapongpra
module load anaconda
conda activate bayeswave-cpp-copy

for config in "${FRAMES_BASE}"/*/config.ini; do
    subdir="$(dirname "$config")"
    echo "=== Running ${subdir##*/} ==="
    bayeswave-cpp-pipe \
        --config_file "$config" \
        --output_directory "${subdir}/output"
done
