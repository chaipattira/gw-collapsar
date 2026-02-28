#!/bin/bash
# Fix relative paths in bayeswave.run files to absolute paths.
# Replaces:
#   --data-directory cached_data_0  -> --data-directory /full/path/to/cached_data_0
#   --outputDir bayeswave_output_0  -> --outputDir /full/path/to/bayeswave_output_0

FRAMES_DIR="/anvil/scratch/x-ctirapongpra/gw-collapsar/Frames_1000"

find "$FRAMES_DIR" -name "bayeswave.run" | while read -r runfile; do
    # The frame directory is two levels up from bayeswave.run
    # e.g. Frames/dur_04s_amp_1.25/bayeswave_output_0/bayeswave.run -> Frames/dur_04s_amp_1.25
    frame_dir="$(dirname "$(dirname "$runfile")")"

    abs_cached="${frame_dir}/cached_data_0"
    abs_output="${frame_dir}/bayeswave_output_0"

    # Only modify the Command line (line 1) relative paths
    sed -i \
        -e "s|--data-directory cached_data_0|--data-directory ${abs_cached}|g" \
        -e "s|--outputDir bayeswave_output_0|--outputDir ${abs_output}|g" \
        "$runfile"

    echo "Updated: $runfile"
done
