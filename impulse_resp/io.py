def parse_cir_multitrace_file(filename):
    import numpy as np
    from collections import defaultdict

    time_base = None
    traces = defaultdict(list)
    metadata = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(',#') or line.startswith('#'):
                continue

            if 't [s]' in line and 'U f [Hz]' in line:
                parts = line.split(',')[6:]
                time_base = np.array([float(x.strip()) for x in parts if x.strip()])
                continue

            if ':' in line and not line.startswith(',S'):
                parts = line.lstrip(',#').split(':')
                if len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip().lstrip('+')
                    try:
                        metadata[key] = float(val)
                    except ValueError:
                        metadata[key] = val
                continue

            if line.startswith(',S'):
                parts = line.split(',')
                trace_id = parts[1].strip()
                values = [float(x) for x in parts[6:] if x.strip()]
                traces[trace_id].append(np.array(values))

    if time_base is None:
        raise ValueError("Time base not found in file")

    return metadata, time_base, traces
