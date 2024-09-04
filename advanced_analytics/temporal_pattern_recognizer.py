import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class TemporalPatternRecognizer:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("TemporalPatternRecognizer")
        self.error_handler = ErrorHandler()

    def detect_seasonality(self, time_series, period):
        try:
            result = seasonal_decompose(time_series, model='additive', period=period)
            return result.seasonal
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting seasonality")
            return None

    def detect_cycles(self, time_series, min_period=2, max_period=50):
        try:
            fft = np.fft.fft(time_series)
            power_spectrum = np.abs(fft) ** 2
            frequencies = np.fft.fftfreq(len(time_series))
            
            positive_freq_idx = np.where(frequencies > 0)[0]
            positive_frequencies = frequencies[positive_freq_idx]
            positive_power_spectrum = power_spectrum[positive_freq_idx]
            
            peak_idx = np.argmax(positive_power_spectrum)
            peak_frequency = positive_frequencies[peak_idx]
            
            if min_period <= 1/peak_frequency <= max_period:
                return 1/peak_frequency
            else:
                return None
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting cycles")
            return None

    def detect_trends(self, time_series):
        try:
            x = np.arange(len(time_series))
            slope, intercept = np.polyfit(x, time_series, 1)
            
            if slope > 0:
                trend = "Increasing"
            elif slope < 0:
                trend = "Decreasing"
            else:
                trend = "Stable"
            
            return {
                'trend': trend,
                'slope': slope,
                'intercept': intercept
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting trends")
            return None

    def detect_anomalies(self, time_series, window_size=10, threshold=2):
        try:
            rolling_mean = np.convolve(time_series, np.ones(window_size), 'valid') / window_size
            rolling_std = np.std(time_series)
            
            anomalies = []
            for i in range(len(time_series) - window_size + 1):
                if abs(time_series[i+window_size-1] - rolling_mean[i]) > threshold * rolling_std:
                    anomalies.append(i+window_size-1)
            
            return anomalies
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting anomalies")
            return []