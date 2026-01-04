#!/usr/bin/env python3
"""
ABOUTME: Standalone script to generate config.ini files for each Frame subfolder.
ABOUTME: Reads trigtime from cache files and generates configs without template dependency.
"""

import os
from pathlib import Path

# Define base paths
BASE_DIR = Path("/home/x-ctirapongpra/scratch/gw-collapsar")
FRAMES_DIR = BASE_DIR / "Frames"

# Embedded config template
CONFIG_TEMPLATE = """[condor]
accounting_group=
accounting_group_user=

[executables]
create_data=/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/create_data
bayeswave=/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/main
#bayeswave_post=/home/x-ctirapongpra/scratch/.conda/envs/2024.02-py311/bayeswave-cpp/bin/bayeswave-cpp-post

[data]
ifo-list=["H1", "L1"]
channel-dict={ "H1":"H1:GW-H", "L1":"L1:GW-L"}
cache-dict={"H1":"/home/x-ctirapongpra/scratch/gw-collapsar/H1.cache", "L1":"/home/x-ctirapongpra/scratch/gw-collapsar/L1.cache"}
psd-dict={"H1":"/home/x-ctirapongpra/scratch/gw-collapsar/H1_psd.dat", "L1":"/home/x-ctirapongpra/scratch/gw-collapsar/L1_psd.dat"}
srate=4096.0
seglen=4.0
# required for simulating data, doesn't do anything,
# but still required when not
dataseed=1272
# only one of the following trigtime or segment-start are required
# usually they are related by trigtime = segment-start + seglen - 2
# but they don't have to be
trigtime=1126259462

flow-dict={"H1": 20.0, "L1": 20.0}
fhigh-dict={"H1": 1024.0, "L1": 1024.0}

# reduces lalsuite output files
dont-dump-extras=
# overwrites the data directory if it aleady exists
overwrite=

[bayeswave.model_settings]
; for gw wavelets model
gw-wavelets=
waveletDmin=1
waveletDmax=20
waveletSNRmin=5
waveletSNRmax=100
printWaveforms=

[bayeswave.run_settings]
Niter=1000000
Nchain=20
Nthread=20

;[bayeswave_post]
;recompute=
;N_waveform_draws=all
;burn_in=100
"""

def get_subfolders():
    """Get all dur_* subdirectories from FRAMES_DIR."""
    subfolders = []
    for item in sorted(FRAMES_DIR.iterdir()):
        if item.is_dir() and item.name.startswith("dur_"):
            subfolders.append(item.name)
    return subfolders


def extract_duration(subfolder_name):
    """Extract duration in seconds from folder name like 'dur_08s_amp_1.25'."""
    duration_str = subfolder_name.split('_')[1].replace('s', '')
    return int(duration_str)


def read_trigtime_from_cache(h1_cache_path, l1_cache_path):
    """
    Read trigtime from both H1 and L1 cache files and validate they match.

    Cache file format (space-delimited):
    <type> <channel> <trigtime> <duration> <path_to_gwf>

    Returns:
        int: The trigtime value from the cache files

    Raises:
        FileNotFoundError: If either cache file doesn't exist
        ValueError: If trigtimes don't match between H1 and L1
    """
    # Read H1 cache file
    if not os.path.exists(h1_cache_path):
        raise FileNotFoundError(f"H1 cache file not found: {h1_cache_path}")

    with open(h1_cache_path, 'r') as f:
        h1_line = f.readline().strip()

    # Read L1 cache file
    if not os.path.exists(l1_cache_path):
        raise FileNotFoundError(f"L1 cache file not found: {l1_cache_path}")

    with open(l1_cache_path, 'r') as f:
        l1_line = f.readline().strip()

    # Parse trigtime from column 3 (index 2)
    h1_trigtime = int(h1_line.split()[2])
    l1_trigtime = int(l1_line.split()[2])

    # Validate that both trigtimes match
    if h1_trigtime != l1_trigtime:
        raise ValueError(
            f"Trigtime mismatch: H1={h1_trigtime}, L1={l1_trigtime} "
            f"in {h1_cache_path} and {l1_cache_path}"
        )

    return h1_trigtime


def generate_config(subfolder_name):
    """Generate a config.ini file for the specified subfolder."""
    # Extract duration
    duration = extract_duration(subfolder_name)
    seglen = float(duration)

    # Define paths for this subfolder
    subfolder_path = FRAMES_DIR / subfolder_name
    cache_h1 = f"/home/x-ctirapongpra/scratch/gw-collapsar/Frames/{subfolder_name}/H1.cache"
    cache_l1 = f"/home/x-ctirapongpra/scratch/gw-collapsar/Frames/{subfolder_name}/L1.cache"
    psd_h1 = f"/home/x-ctirapongpra/scratch/gw-collapsar/Frames/{subfolder_name}/H1_psd.dat"
    psd_l1 = f"/home/x-ctirapongpra/scratch/gw-collapsar/Frames/{subfolder_name}/L1_psd.dat"

    # Read trigtime from cache files
    trigtime = read_trigtime_from_cache(cache_h1, cache_l1)

    # Start with template content
    modified_content = CONFIG_TEMPLATE

    # Replace seglen
    modified_content = modified_content.replace("seglen=4.0", f"seglen={seglen}")

    # Replace cache-dict
    old_cache = 'cache-dict={"H1":"/home/x-ctirapongpra/scratch/gw-collapsar/H1.cache", "L1":"/home/x-ctirapongpra/scratch/gw-collapsar/L1.cache"}'
    new_cache = f'cache-dict={{"H1":"{cache_h1}", "L1":"{cache_l1}"}}'
    modified_content = modified_content.replace(old_cache, new_cache)

    # Replace psd-dict
    old_psd = 'psd-dict={"H1":"/home/x-ctirapongpra/scratch/gw-collapsar/H1_psd.dat", "L1":"/home/x-ctirapongpra/scratch/gw-collapsar/L1_psd.dat"}'
    new_psd = f'psd-dict={{"H1":"{psd_h1}", "L1":"{psd_l1}"}}'
    modified_content = modified_content.replace(old_psd, new_psd)

    # Replace trigtime
    modified_content = modified_content.replace("trigtime=1126259462", f"trigtime={trigtime}")

    # Write to subfolder
    output_path = subfolder_path / "config.ini"
    with open(output_path, 'w') as f:
        f.write(modified_content)

    print(f"Created {output_path}")
    return output_path


def main():
    """Generate config.ini files for all Frame subfolders."""
    subfolders = get_subfolders()

    print("Generating config.ini files for Frame subfolders...")
    print(f"Output directory: {FRAMES_DIR}")
    print(f"Found {len(subfolders)} dur_* subdirectories")
    print()

    for subfolder in subfolders:
        output_path = generate_config(subfolder)

    print()
    print(f"Successfully created {len(subfolders)} config.ini files.")


if __name__ == "__main__":
    main()
