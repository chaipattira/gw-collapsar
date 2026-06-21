#!/usr/bin/env python3
from pathlib import Path

FRAMES_DIR = Path("/anvil/scratch/x-ctirapongpra/gw-collapsar/three_detectors")
PSD_DIR    = Path("/anvil/scratch/x-ctirapongpra/gw-collapsar/PSD")

DETECTORS = {
    'H1': 'H1:GW-H',
    'L1': 'L1:GW-L',
    'V1': 'V1:GW-V',
}


def read_gps_start(cache_path):
    with open(cache_path) as f:
        return int(f.readline().split()[2])


def generate_config(name):
    subfolder = FRAMES_DIR / name
    duration  = 32

    gps_values = {}
    for det in DETECTORS:
        gps_values[det] = read_gps_start(subfolder / f"{det}.cache")

    unique = set(gps_values.values())
    if len(unique) > 1:
        raise ValueError(f"{name}: GPS mismatch {gps_values}")

    gps_start = gps_values['H1']
    trigtime  = gps_start + duration // 2

    ifo_list     = str(list(DETECTORS.keys())).replace("'", '"')
    channel_dict = ", ".join(f'"{d}":"{c}"' for d, c in DETECTORS.items())
    cache_dict   = ", ".join(f'"{d}":"{subfolder}/{d}.cache"' for d in DETECTORS)
    psd_dict     = ", ".join(f'"{d}":"{PSD_DIR}/{d}_psd.dat"' for d in DETECTORS)
    flow_dict    = ", ".join(f'"{d}": 22.0' for d in DETECTORS)
    fhigh_dict   = ", ".join(f'"{d}": 1023.75' for d in DETECTORS)

    config = f"""[condor]
accounting_group=
accounting_group_user=

[executables]
create_data=/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/create_data
bayeswave=/home/x-ctirapongpra/scratch/bayeswave-cpp/build/src/main
bayeswave_post=/anvil/scratch/x-ctirapongpra/.conda/envs/2024.02-py311/bayeswave-cpp-copy/bin/bayeswave-cpp-post

[data]
ifo-list={ifo_list}
channel-dict={{{channel_dict}}}
cache-dict={{{cache_dict}}}
psd-dict={{{psd_dict}}}
srate=2048.0
seglen={duration}.0
dataseed=1272
segment-start={gps_start}
trigtime={trigtime}
psdlength={duration}.0
psdstart={gps_start}

flow-dict={{{flow_dict}}}
fhigh-dict={{{fhigh_dict}}}

dont-dump-extras=
overwrite=

[bayeswave.model_settings]
gw-wavelets=
waveletDmin=1
waveletDmax=400
waveletSNRmin=5
waveletSNRmax=200
printWaveforms=
checkpointingIntervalHrs=24

[bayeswave.run_settings]
Niter=5000000
Nchain=20
Nthread=20

[bayeswave_post]
recompute=
N_waveform_draws=all
burn_in=half
"""
    path = subfolder / "config.ini"
    path.write_text(config)
    print(f"Created {path}")


def main():
    subfolders = sorted(d.name for d in FRAMES_DIR.iterdir()
                        if d.is_dir() and d.name.startswith("full_signal_"))
    for name in subfolders:
        generate_config(name)


if __name__ == "__main__":
    main()
