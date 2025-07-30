def plot_trace_block(time, trace_dict, rep_idx=0):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for trace_name in sorted(trace_dict.keys()):
        if rep_idx < len(trace_dict[trace_name]):
            plt.plot(time * 1e9, trace_dict[trace_name][rep_idx], label=trace_name)

    plt.xlabel("Time [ns]")
    plt.ylabel("Amplitude [dB]")
    plt.title(f"CIR Measurement Block #{rep_idx + 1}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def animate_traces(time, trace_dict, interval=0.1):
    import matplotlib.pyplot as plt
    import time as pytime

    num_frames = min(len(v) for v in trace_dict.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    lines = {}

    # Initial plot
    for trace_name in sorted(trace_dict.keys()):
        y = trace_dict[trace_name][0]
        line, = ax.plot(time * 1e9, y, label=trace_name)
        lines[trace_name] = line

    ax.set_xlabel("Time [ns]")
    ax.set_ylabel("Amplitude [dB]")
    ax.set_title("CIR Animation")
    ax.legend()
    ax.grid(True)

    for i in range(num_frames):
        for trace_name, line in lines.items():
            line.set_ydata(trace_dict[trace_name][i])
        ax.set_title(f"CIR Animation - Frame {i + 1}/{num_frames}")
        plt.pause(interval)
        pytime.sleep(interval)

    plt.show()
