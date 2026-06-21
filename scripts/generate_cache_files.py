import os
import glob
from gwpy.timeseries import TimeSeries

DETECTORS = {
    'H1': {'channel': 'H1:GW-H', 'code': 'H'},
    'L1': {'channel': 'L1:GW-L', 'code': 'L'},
    'V1': {'channel': 'V1:GW-V', 'code': 'V'},
}

BASE_DIR = '/anvil/scratch/x-ctirapongpra/gw-collapsar/three_detectors'


def main():
    signal_dirs = sorted(glob.glob(os.path.join(BASE_DIR, 'full_signal_*')))
    if not signal_dirs:
        print("No full_signal_* subdirectories found!")
        return

    for signal_dir in signal_dirs:
        for det, cfg in DETECTORS.items():
            gwf = os.path.join(signal_dir, f'{det}.gwf')
            if not os.path.exists(gwf):
                print(f"WARNING: {gwf} not found!")
                continue

            ts = TimeSeries.read(gwf, channel=cfg['channel'])
            line = f"{cfg['code']} {cfg['channel']} {int(ts.t0.value)} {int(ts.duration.value)} {os.path.abspath(gwf)}"

            cache = os.path.join(signal_dir, f'{det}.cache')
            with open(cache, 'w') as f:
                f.write(line + '\n')
            print(f"Created: {cache}")


if __name__ == '__main__':
    main()
