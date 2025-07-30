# Channel Impulse Response (CIR) Analyzer

This repository processes and analyzes Channel Impulse Response (CIR) data collected from a **Keysight PNA N5227B** vector network analyzer. The setup consists of **two antennas with orthogonal TX/RX paths**, producing four S-parameter traces: `S31`, `S32`, `S41`, and `S42`.

The measurement tracks how the **impulse response evolves over frequency** while keeping the physical propagation channel static. The code is built on top of **scikit-rf**, `matplotlib`, and `numpy`.

---

## 🧩 Code Structure

### `impulse_resp/io.py`
- `parse_cir_multitrace_file(filename)`
  - Parses native VNA `.csv` files exported from the Keysight interface.
  - Extracts `time_base`, metadata, and multi-repetition trace data grouped by S-parameter.
  - Returns: `metadata: dict`, `time: np.ndarray`, `traces: dict[str, list[np.ndarray]]`

### `impulse_resp/metrics.py`
- `analyze_cir(time: np.ndarray, db_vals: np.ndarray, threshold_dB: float = 20)`
  - Computes delay spread characteristics:
    - `mu_tau_ns`: Mean excess delay [ns]
    - `rms_tau_ns`: RMS delay spread [ns]
    - `multipath_components`: Number of paths above threshold (default: -20 dB)
    - `max_excess_delay_ns`: Time span between first and last significant path
    - `coherence_bw_MHz`: Coherence bandwidth (from RMS delay spread)
    - `energy_pct_first_20ns`: % of total energy concentrated in first 20 ns
    - `total_pwr_linear`: Total received power (linear scale)
    - `pdp_kurtosis`: Sharpness/sparseness of the power delay profile
    - `avg_power_dB`: Average received power
    - `peak_power_dB`: Peak received power

  - Returns a dictionary of metrics.

### `impulse_resp/plotting.py`
- `plot_trace_block(time, trace_dict, rep_idx=0)`
  - Plots a single measurement block (repetition) for all traces in the time domain.
- `animate_traces(time, trace_dict, interval=0.1)`
  - Shows an animation of multiple measurement blocks across time.

---

## 🚀 CLI Usage

```bash
python -m scripts.analyze wyniki/Results_20250505091345.txt [--animate]
````

### Example output:

```
== S31 ==
Average delay: 27.2 ns
== S32 ==
Average delay: 25.8 ns
...

=== ITU-R Style Multipath Summary ===
trace   mu_tau_ns  rms_tau_ns  max_excess_delay_ns  multipath_components  coherence_bw_MHz  energy_pct_first_20ns  pdp_kurtosis  avg_power_dB  peak_power_dB
 S31       27.18        6.82               45.11                    19              25.19                   87.1          3.72         -84.56          -47.92
 S32       25.66        5.49               40.35                    17              30.82                   88.5          4.05         -86.10          -51.28
 ...
```

---

## 📊 ITU-R Compliance Metrics

The following channel metrics are reported per \[ITU-R Rec. P.1407 / P.1238 / P.2040]:

| Metric                | Description                                                               |
| --------------------- | ------------------------------------------------------------------------- |
| Mean Excess Delay     | Center of energy delay (μₜ)                                               |
| RMS Delay Spread      | Standard deviation of delay (σₜ)                                          |
| Max Excess Delay      | Span of significant paths (typically > -20 dB from peak)                  |
| Multipath Components  | Number of reflections above threshold                                     |
| Coherence Bandwidth   | $B_c = \frac{1}{5 \cdot \sigma_τ}$ in MHz                                 |
| Energy in First 20 ns | Percentage of total power received in the first 20 ns                     |
| PDP Kurtosis          | Indicates sparseness or fat-tailed behavior of the multipath distribution |
| Average Power \[dB]   | Mean total power                                                          |
| Peak Power \[dB]      | Maximum received amplitude                                                |

---

## 🛠 Dependencies

Install via:

```bash
pip install -r requirements.txt
```

* `numpy`
* `matplotlib`
* `pandas`
* `scipy`
* `scikit-rf` *(optional for future extensions)*

---

## 📁 Project Layout

```
impulse_resp/
├── io.py         # File parsing logic
├── metrics.py    # Delay spread + ITU-style metrics
├── plotting.py   # Visualization tools
scripts/
└── analyze.py       # CLI runner
```

---

## 📌 Future Directions

* Frequency vs. RMS delay & coherence bandwidth plots
* Delay spread CDFs across frequency bins
* Export to standardized IEEE-style CSV format
* Direct `.sNp` support via `skrf.Network`
* PDF or LaTeX report generation
