def analyze_cir(time, db_vals, threshold_dB=20, energy_window_ns=20):
    import numpy as np
    from scipy.stats import kurtosis

    pwr = 10 ** (db_vals / 10)
    pwr_sum = np.sum(pwr)

    if pwr_sum == 0:
        return None

    mu_tau = np.sum(time * pwr) / pwr_sum
    sigma_tau = np.sqrt(np.sum(((time - mu_tau) ** 2) * pwr) / pwr_sum)

    max_pwr_db = np.max(db_vals)
    significant_mask = db_vals > (max_pwr_db - threshold_dB)
    multipath_count = np.sum(significant_mask)

    if np.any(significant_mask):
        max_excess_delay = time[significant_mask][-1] - time[significant_mask][0]
    else:
        max_excess_delay = 0.0

    avg_atten_dB = 10 * np.log10(np.mean(pwr))
    peak_dB = max_pwr_db

    # Coherence bandwidth (Hz)
    coherence_bw_Hz = 1 / (5 * sigma_tau) if sigma_tau > 0 else 0

    # Energy concentration in first N ns
    energy_window_s = energy_window_ns * 1e-9
    early_mask = time <= energy_window_s
    energy_pct_first_N = (np.sum(pwr[early_mask]) / pwr_sum) * 100

    # Total PDP energy (linear)
    total_pwr = pwr_sum

    # Kurtosis of PDP
    pdp_kurtosis = kurtosis(pwr, fisher=False)

    return {
        'mu_tau_ns': mu_tau * 1e9,
        'rms_tau_ns': sigma_tau * 1e9,
        'multipath_components': multipath_count,
        'avg_power_dB': avg_atten_dB,
        'peak_power_dB': peak_dB,
        'max_excess_delay_ns': max_excess_delay * 1e9,
        'coherence_bw_MHz': coherence_bw_Hz / 1e6,
        'energy_pct_first_20ns': energy_pct_first_N,
        'total_pwr_linear': total_pwr,
        'pdp_kurtosis': pdp_kurtosis
    }
    
