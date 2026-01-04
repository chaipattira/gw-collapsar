# ABOUTME: Shell script to run bayeswave-cpp-pipe for all 9 Frame configurations
# ABOUTME: Each Frame will have its output directory created inside its subfolder
# sh /home/x-ctirapongpra/scratch/gw-collapsar/scripts/run_all_bayeswave.sh

set -e  # Exit on error

source ~/.bashrc 
conda activate bayeswave-cpp

# Define paths
BAYESWAVE_DIR="/anvil/scratch/x-ctirapongpra/bayeswave-cpp"
FRAMES_BASE="/home/x-ctirapongpra/scratch/gw-collapsar/Frames"

# List of all Frame subfolders
SUBFOLDERS=(
    "dur_04s_amp_1.25"
    "dur_04s_amp_2.50"
    "dur_04s_amp_5.00"
    "dur_08s_amp_1.25"
    "dur_08s_amp_2.50"
    "dur_08s_amp_5.00"
    "dur_16s_amp_1.25"
    "dur_16s_amp_2.50"
    "dur_16s_amp_5.00"
    "dur_32s_amp_1.25"
    "dur_32s_amp_2.50"
    "dur_32s_amp_5.00"
)

# Change to bayeswave-cpp directory
cd "$BAYESWAVE_DIR" || { echo "Failed to change to $BAYESWAVE_DIR"; exit 1; }

# Counter for tracking progress
TOTAL=${#SUBFOLDERS[@]}
CURRENT=0

echo "Running BayesWave analysis on $TOTAL Frame configurations"
echo ""

# Loop through each subfolder
for subfolder in "${SUBFOLDERS[@]}"; do
    CURRENT=$((CURRENT + 1))

    CONFIG_FILE="${FRAMES_BASE}/${subfolder}/config.ini"
    OUTPUT_DIR="${FRAMES_BASE}/${subfolder}/output"

    echo "[$CURRENT/$TOTAL] Processing: $subfolder"

    # Run bayeswave-cpp-pipe
    if bayeswave-cpp-pipe \
        --config_file "$CONFIG_FILE" \
        --output_directory "$OUTPUT_DIR"; then
        echo "  Successfully completed $subfolder"
    else
        EXIT_CODE=$?
        echo "  FAILED: $subfolder (exit code: $EXIT_CODE)"
        echo "  Continuing with remaining configurations..."
    fi

    echo ""
done

echo "Batch processing complete!"
echo "========================================"