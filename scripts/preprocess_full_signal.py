#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from gwpy.timeseries import TimeSeries

# --- Config ---
DATA_DIR    = '/home/x-ctirapongpra/scratch/gw-collapsar/injected_signal'
OUTPUT_DIR  = '/anvil/scratch/x-ctirapongpra/gw-collapsar/three_detectors'
AXIS        = 'z'
AMP_FACTORS = {
    'x': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
    'z': [0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
}
PAD_DUR     = 4.0
MAKE_PLOT   = True

SCALE       = 1e-23
SRATE       = 4096
TAPER_DUR   = 0.5

DETECTORS = {
    'H1': {'channel': 'H1:GW-H', 't0': 1126259462.423,     'Fp':  0.578742411175002,   'Fx': -0.4509478210953121, 'color': 'blue'},
    'L1': {'channel': 'L1:GW-L', 't0': 1126259462.4160156, 'Fp': -0.5274334329518102,  'Fx':  0.20520960891727436, 'color': 'orange'},
    'V1': {'channel': 'V1:GW-V', 't0': 1126259462.4187396, 'Fp': -0.46399483825405136, 'Fx':  0.4040119180250937, 'color': 'green'},
}


def plot_signals(configs, output_dir, axis):
    n = len(configs)
    ndets = len(DETECTORS)
    fig, axes = plt.subplots(n, ndets, figsize=(8 * ndets, 4 * n))
    if n == 1:
        axes = axes.reshape(1, -1)

    for i, cfg in enumerate(configs):
        for j, det in enumerate(DETECTORS):
            d = DETECTORS[det]
            ax = axes[i, j]
            ts = cfg['ts'][det]
            ax.plot(ts.times.value - d['t0'], ts.value / 1e-21, lw=0.5, color=d['color'])
            ax.set_title(f"{det}: amp={cfg['amp']:.2f}")
            ax.set_ylabel('Strain ($10^{-21}$)')
            ax.grid(True, alpha=0.3)
            ax.axvline(0, color='red', ls='--', lw=1.5, alpha=0.7, label='$t_0$')
            if i == n - 1:
                ax.set_xlabel('Time relative to $t_0$ (s)')
            if i == 0 and j == 0:
                ax.legend(loc='upper right')

    plt.tight_layout()
    path = os.path.join(output_dir, f'preprocessed_signals_{axis}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"Plot saved: {path}")
    plt.show()


def preprocess_full_signal():
    # Load raw data
    t = np.loadtxt(os.path.join(DATA_DIR, 't.txt'), delimiter=',')
    hp = np.loadtxt(os.path.join(DATA_DIR, f'hp_{AXIS}.txt'))
    hx = np.loadtxt(os.path.join(DATA_DIR, f'hx_{AXIS}.txt'))
    dt = t[1] - t[0]
    sr = 1.0 / dt

    # Build per-detector TimeSeries
    raw = {}
    for det, d in DETECTORS.items():
        h = d['Fp'] * hp + d['Fx'] * hx
        n = len(h)
        raw[det] = TimeSeries(h, sample_rate=sr, t0=d['t0'] - (n - 1) * dt / 2,
                              name=d['channel'], unit='strain')

    orig_dur = raw['H1'].duration.value
    target_dur = orig_dur + 2 * PAD_DUR

    configs = []
    for amp in AMP_FACTORS[AXIS]:
        out = os.path.join(OUTPUT_DIR, f"full_signal_{AXIS}_amp_{amp:.2f}")
        os.makedirs(out, exist_ok=True)
        ts_dict = {}

        for det, ts in raw.items():
            ts_s = ts * SCALE * amp
            ts_r = ts_s.resample(SRATE)

            n = len(ts_r)
            alpha = min(2.0 * TAPER_DUR * SRATE / n, 1.0)
            ts_t = ts_r * signal.windows.tukey(n, alpha=alpha)

            pad = int(PAD_DUR * SRATE)
            ts_p = ts_t.pad((pad, pad))

            t0_int = int(DETECTORS[det]['t0'])
            ts_p.shift(t0_int - target_dur / 2.0 - ts_p.t0.value)

            fname = os.path.join(out, f'{det}.gwf')
            ts_p.write(fname, format='gwf')
            print(f"Written: {fname}  ({ts_p.duration.value:.1f}s, GPS {ts_p.t0.value:.3f})")
            ts_dict[det] = ts_p

        configs.append({'ts': ts_dict, 'amp': amp})

    if MAKE_PLOT:
        plot_signals(configs, OUTPUT_DIR, AXIS)


if __name__ == '__main__':
    preprocess_full_signal()
