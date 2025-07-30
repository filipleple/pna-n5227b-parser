def analyze_cir(time, db_vals, threshold_dB=20):
    import numpy as np

    pwr = 10 ** (db_vals / 10)
    pwr_sum = np.sum(pwr)

    mu_tau = np.sum(time * pwr) / pwr_sum
    sigma_tau = np.sqrt(np.sum(((time - mu_tau) ** 2) * pwr) / pwr_sum)

    max_pwr_db = np.max(db_vals)
    multipath_count = np.sum(db_vals > (max_pwr_db - threshold_dB))

    avg_atten_dB = 10 * np.log10(np.mean(pwr))
    peak_dB = np.max(db_vals)

    return {
        'mu_tau_ns': mu_tau * 1e9,
        'rms_tau_ns': sigma_tau * 1e9,
        'multipath_components': multipath_count,
        'avg_power_dB': avg_atten_dB,
        'peak_power_dB': peak_dB
    }

