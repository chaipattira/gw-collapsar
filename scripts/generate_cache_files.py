# ABOUTME: Generates LIGO cache files for each dur_* subdirectory in Frames/
# ABOUTME: Extracts GPS start time and duration directly from GWF files using gwpy

import os
import glob
from gwpy.timeseries import TimeSeries

# Detector configuration
DETECTORS = {
    'H1': {
        'channel_name': 'H1:GW-H',
        'detector_code': 'H'
    },
    'L1': {
        'channel_name': 'L1:GW-L',
        'detector_code': 'L'
    }
}

def generate_cache_file(gwf_path, detector_name, detector_config):
    """
    Generate a cache file entry for a GWF file.

    Args:
        gwf_path: Path to the GWF file
        detector_name: Name of the detector (e.g., 'H1', 'L1')
        detector_config: Configuration dict with channel_name and detector_code

    Returns:
        Formatted cache file line as a string
    """
    # Read the GWF file to extract metadata (need to specify channel)
    ts = TimeSeries.read(gwf_path, channel=detector_config['channel_name'])

    # Extract GPS start time and duration
    gps_start = int(ts.t0.value)
    duration = int(ts.duration.value)

    # Get absolute path to GWF file
    abs_path = os.path.abspath(gwf_path)

    # Format: [DETECTOR] [CHANNEL_NAME] [GPS_START_TIME] [DURATION_SECONDS] [PATH_TO_GWF_FILE]
    cache_line = f"{detector_config['detector_code']} {detector_config['channel_name']} {gps_start} {duration} {abs_path}"

    return cache_line

def main():
    # Base directory containing all dur_* subdirectories
    base_dir = '/anvil/scratch/x-ctirapongpra/gw-collapsar/Frames_400'

    # Find all dur_* subdirectories
    dur_dirs = sorted(glob.glob(os.path.join(base_dir, 'dur_*')))

    if not dur_dirs:
        print("No dur_* subdirectories found!")
        return

    print(f"Found {len(dur_dirs)} dur_* subdirectories")
    print("=" * 70)

    # Process each subdirectory
    for dur_dir in dur_dirs:
        dir_name = os.path.basename(dur_dir)
        print(f"\nProcessing: {dir_name}")

        # Process each detector
        for detector_name, detector_config in DETECTORS.items():
            # Path to GWF file
            gwf_file = os.path.join(dur_dir, f'{detector_name}.gwf')

            if not os.path.exists(gwf_file):
                print(f"  WARNING: {gwf_file} not found!")
                continue

            # Generate cache line
            cache_line = generate_cache_file(gwf_file, detector_name, detector_config)

            # Write cache file
            cache_file = os.path.join(dur_dir, f'{detector_name}.cache')
            with open(cache_file, 'w') as f:
                f.write(cache_line + '\n')

            print(f"  Created: {detector_name}.cache")

    print("\n" + "=" * 70)
    print("Cache file generation complete!")
    print(f"Generated cache files for {len(dur_dirs)} subdirectories")

if __name__ == '__main__':
    main()