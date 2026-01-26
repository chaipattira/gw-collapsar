#!/usr/bin/env python3
"""
ABOUTME: Standalone script to generate config.ini files for each Frame subfolder.
ABOUTME: Reads GPS times from cache files and generates configs with correct timing parameters.
"""

from pathlib import Path

BASE_DIR = Path("/home/x-ctirapongpra/scratch/gw-collapsar")
FRAMES_DIR = BASE_DIR / "Frames"


def read_gps_start(cache_path):
    """Read GPS start time from cache file (column 3)."""
    with open(cache_path) as f:
        return int(f.readline().split()[2])


def generate_config(subfolder_name):
    """Generate config.ini for a Frame subfolder."""
    subfolder = FRAMES_DIR / subfolder_name

    # Extract duration from folder name (e.g., "dur_08s_amp_1.25" -> 8)
    duration = int(subfolder_name.split('_')[1].replace('s', ''))

    # Read GPS start time from cache and verify both detectors match
    gps_h1 = read_gps_start(subfolder / "H1.cache")
    gps_l1 = read_gps_start(subfolder / "L1.cache")
    if gps_h1 != gps_l1:
        raise ValueError(f"{subfolder_name}: GPS mismatch H1={gps_h1}, L1={gps_l1}")

    # Calculate timing parameters
    gps_start = gps_h1
    trigtime = gps_start + duration

    # Generate config content
    config = f"""[condor]
accounting_group=
accounting_group_user=

[executables]
create_data=/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/create_data
bayeswave=/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/main
#bayeswave_post=/home/x-ctirapongpra/scratch/.conda/envs/2024.02-py311/bayeswave-cpp/bin/bayeswave-cpp-post

[data]
ifo-list=["H1", "L1"]
channel-dict={{ "H1":"H1:GW-H", "L1":"L1:GW-L"}}
cache-dict={{"H1":"{subfolder}/H1.cache", "L1":"{subfolder}/L1.cache"}}
psd-dict={{"H1":"{subfolder}/H1_psd.dat", "L1":"{subfolder}/L1_psd.dat"}}
srate=4096.0
seglen={duration}.0
dataseed=1272
segment-start={gps_start}
trigtime={trigtime}.0
psdlength={duration}.0
psdstart={gps_start}

flow-dict={{"H1": 20.0, "L1": 20.0}}
fhigh-dict={{"H1": 1024.0, "L1": 1024.0}}

dont-dump-extras=
overwrite=

[bayeswave.model_settings]
gw-wavelets=
waveletDmin=1
waveletDmax=400
waveletSNRmin=5
waveletSNRmax=200
printWaveforms=
verbose=
checkpointingIntervalHrs=12

[bayeswave.run_settings]
Niter=4000000
Nchain=20
Nthread=20

;[bayeswave_post]
;recompute=
;N_waveform_draws=all
;burn_in=100
"""

    # Write config file
    output_path = subfolder / "config.ini"
    output_path.write_text(config)
    print(f"Created {output_path}")


def main():
    """Generate config.ini files for all Frame subfolders."""
    subfolders = sorted([d.name for d in FRAMES_DIR.iterdir()
                        if d.is_dir() and d.name.startswith("dur_")])

    print(f"Generating {len(subfolders)} config files in {FRAMES_DIR}")
    print()

    for subfolder in subfolders:
        generate_config(subfolder)

    print(f"\nSuccessfully created {len(subfolders)} config.ini files.")


if __name__ == "__main__":
    main()
