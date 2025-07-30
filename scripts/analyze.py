from impulse_resp.io import parse_cir_multitrace_file
from impulse_resp.metrics import analyze_cir
from impulse_resp.plotting import plot_trace_block, animate_traces

import argparse
import numpy as np

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

plot_trace_block(time, {k: v for k, v in traces.items()})

if args.animate:
    animate_traces(time, traces)
