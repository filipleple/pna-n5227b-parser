import numpy as np
import matplotlib.pyplot as plt

def parse_keysight_cir_csv(filename):
    metadata = {}
    data_line = None

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse metadata
            if line.startswith(',#') or line.startswith('#'):
                continue
            if ':' in line:
                parts = line.lstrip(',#').split(':')
                if len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip().lstrip('+')
                    try:
                        metadata[key] = float(val)
                    except ValueError:
                        metadata[key] = val

            # Look for data line starting with ',S41'
            if line.startswith(',S41'):
                data_line = line
                break

    if data_line is None:
        raise ValueError("Could not find CIR data line starting with ',S41'")

    # Extract values after trace label and padding
    parts = data_line.split(',')
    data_strs = parts[6:]  # skip ',S41,,,,,'
    data = np.array([float(x) for x in data_strs if x.strip() != ''])

    # Time base from metadata
    sweep_pts = int(metadata.get("No. of sweep points", len(data)))
    time_span = metadata.get("Time SPAN [s]", 1e-7)
    time = np.linspace(0, time_span, sweep_pts)

    return metadata, time, data

# Run it
filename = "wyniki/Results_20250505085444.txt"
meta, t, amp = parse_keysight_cir_csv(filename)

# Display summary
print("CIR metadata:")
for k, v in meta.items():
    print(f"{k}: {v}")

print(f"\nTime array: {t.shape}, Amplitude array: {amp.shape}")

# Plot
plt.plot(t * 1e9, amp)  # convert to ns
plt.xlabel("Time [ns]")
plt.ylabel("Amplitude [dB]" if np.mean(amp) < -50 else "Amplitude (linear)")
plt.title("CIR from Keysight PNA N5227B (S41)")
plt.grid(True)
plt.tight_layout()
plt.show()
