#!/usr/bin/env python3
import numpy as np
import os

PSD_DIR = '/anvil/scratch/x-ctirapongpra/gw-collapsar/PSD'

ASD_FILES = {
    'H1': os.path.join(PSD_DIR, 'AplusDesign.txt'),
    'L1': os.path.join(PSD_DIR, 'AplusDesign.txt'),
    'V1': os.path.join(PSD_DIR, 'VirgoO5Tier1HighSens.txt'),
}

for det, asd_file in ASD_FILES.items():
    data = np.loadtxt(asd_file)
    freq = data[:, 0]
    psd  = data[:, 1] ** 2  # ASD -> PSD

    out = os.path.join(PSD_DIR, f'{det}_psd.dat')
    np.savetxt(out, np.column_stack([freq, psd]), fmt='%.6e')
    print(f"Written: {out}  ({len(freq)} points, {freq[0]:.1f}–{freq[-1]:.1f} Hz)")
