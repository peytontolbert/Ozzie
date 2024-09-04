from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ForecastingEngine:
    def __init__(self):
        self.logger = Logger("ForecastingEngine")
        self.error_handler = ErrorHandler()

    def arima_forecast(self, time_series, order=(1,1,1), steps=10):
        try:
            model = ARIMA(time_series, order=order)
            results = model.fit()
            forecast = results.forecast(steps=steps)
            return forecast
        except Exception as e:
            self.error_handler.handle_error(e, "Error performing ARIMA forecast")
            return None

    def exponential_smoothing_forecast(self, time_series, seasonal_periods=None, steps=10):
        try:
            if seasonal_periods:
                model = ExponentialSmoothing(time_series, seasonal_periods=seasonal_periods, trend='add', seasonal='add')
            else:
                model = ExponentialSmoothing(time_series, trend='add')
            results = model.fit()
            forecast = results.forecast(steps=steps)
            return forecast
        except Exception as e:
            self.error_handler.handle_error(e, "Error performing Exponential Smoothing forecast")
            return None

    def evaluate_forecast(self, actual, predicted):
        try:
            mse = mean_squared_error(actual, predicted)
            rmse = np.sqrt(mse)
            return {
                'MSE': mse,
                'RMSE': rmse
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error evaluating forecast")
            return None

    def select_best_model(self, time_series, test_size=10):
        try:
            train = time_series[:-test_size]
            test = time_series[-test_size:]
            
            # ARIMA
            arima_forecast = self.arima_forecast(train, steps=test_size)
            arima_error = self.evaluate_forecast(test, arima_forecast)
            
            # Exponential Smoothing
            es_forecast = self.exponential_smoothing_forecast(train, steps=test_size)
            es_error = self.evaluate_forecast(test, es_forecast)
            
            if arima_error['RMSE'] < es_error['RMSE']:
                return 'ARIMA', arima_error
            else:
                return 'Exponential Smoothing', es_error
        except Exception as e:
            self.error_handler.handle_error(e, "Error selecting best model")
            return None