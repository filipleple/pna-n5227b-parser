from impulse_resp.io import parse_cir_multitrace_file
from impulse_resp.metrics import analyze_cir
from impulse_resp.plotting import plot_trace_block, animate_traces

import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Path to CIR CSV file")
parser.add_argument("--animate", action="store_true", help="Show CIR animation")
args = parser.parse_args()

meta, time, traces = parse_cir_multitrace_file(args.file)

for trace_name in traces:
    print(f"== {trace_name} ==")
    results = [analyze_cir(time, trace) for trace in traces[trace_name]]
    avg_delay = np.mean([r["mu_tau_ns"] for r in results])
    print("Average delay:", avg_delay, "ns")


# Accumulate analysis results
rows = []
for trace_name in traces:
    results = [analyze_cir(time, trace) for trace in traces[trace_name]]
    avg = {key: np.mean([r[key] for r in results]) for key in results[0]}
    avg["trace"] = trace_name
    rows.append(avg)

# Create ITU-style summary DataFrame
df = pd.DataFrame(rows)
df = df[["trace", "mu_tau_ns", "rms_tau_ns", "max_excess_delay_ns",
         "multipath_components", "avg_power_dB", "peak_power_dB"]]

print("\n=== ITU-R Style Multipath Summary ===")
print(df.to_string(index=False))

plot_trace_block(time, {k: v for k, v in traces.items()})

if args.animate:
    animate_traces(time, traces)
