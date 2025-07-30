import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_cir_multitrace_file(filename):
    time_base = None
    traces = defaultdict(list)
    metadata = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(',#') or line.startswith('#'):
                continue

            # Extract time base line
            if 't [s]' in line and 'U f [Hz]' in line:
                parts = line.split(',')[6:]  # skip garbage
                time_base = np.array([float(x.strip()) for x in parts if x.strip()])
                continue

            # Metadata
            if ':' in line and not line.startswith(',S'):
                parts = line.lstrip(',#').split(':')
                if len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip().lstrip('+')
                    try:
                        metadata[key] = float(val)
                    except ValueError:
                        metadata[key] = val
                continue

            # Trace line
            if line.startswith(',S'):
                parts = line.split(',')
                trace_id = parts[1].strip()
                values = [float(x) for x in parts[6:] if x.strip()]
                traces[trace_id].append(np.array(values))

    if time_base is None:
        raise ValueError("Time base not found in file")

    return metadata, time_base, traces

# Run it
filename = 'wyniki/Results_20250505085444.txt'
meta, time, trace_dict = parse_cir_multitrace_file(filename)

# Display what we got
print(f"Time base: {len(time)} points")
for key, series in trace_dict.items():
    print(f"{key}: {len(series)} traces, each with {len(series[0])} points")

# Plot one full group (first repetition)
rep_idx = 0
plt.figure(figsize=(10,6))
for trace_name in sorted(trace_dict.keys()):
    if rep_idx < len(trace_dict[trace_name]):
        plt.plot(time * 1e9, trace_dict[trace_name][rep_idx], label=trace_name)
plt.xlabel("Time [ns]")
plt.ylabel("Amplitude [dB]")
plt.title(f"CIR Measurement Block #{rep_idx+1}")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
