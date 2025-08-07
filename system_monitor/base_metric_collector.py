# system_monitor/base_metric_collector.py
from abc import ABC, abstractmethod
import time
import threading
import pandas as pd
import numpy as np # For potential NaN handling if needed in summary

class BaseMetricCollector(ABC):
    """Abstract base class for collecting and summarizing metrics.

    Args:
        name (str): A human-readable name for the collector.
        interval (float, optional): The sampling interval in seconds.

    Attributes:
        _data_points (list[dict]): Stores raw data points collected during a run.
        _is_running (bool): Indicates if the collection thread is running.
        _thread (Thread, None): The background thread that performs data collection.
        _stop_event (Event): Event to signal the thread to stop.

    Methods:
        __init__(self, name: str, interval: float = 0.5):
            Initializes the base metric collector with a name and optional interval.

        _collect_data_point(self) -> dict:
            Abstract method to be implemented by subclasses to collect data points.
            Returns a dictionary of metric names and their values.

        start(self):
            Starts the continuous data collection in a separate thread.

        stop(self) -> list[dict]:
            Stops the data collection thread and returns all collected raw data points.

        get_summary(self) -> dict:
            Processes the collected raw data points and returns a summary."""
    def __init__(self, name: str, interval: float = 0.5):
        """
        Initializes the base metric collector.

        Args:
            name (str): A human-readable name for the collector (e.g., "CPU Monitor").
            interval (float): The sampling interval in seconds (how often to collect data).
        """
        self.name = name
        self.interval = interval
        self._data_points = []  # Stores raw data points collected during a run
        self._is_running = False
        self._thread = None
        self._stop_event = threading.Event() # Event to signal the thread to stop

    @abstractmethod
    def _collect_data_point(self) -> dict:
        """
        Abstract method to be implemented by subclasses.
        Should return a dictionary of collected metric names and their values.
        """
        pass

    def _run_collection(self):
        """Internal method to run data collection in a separate thread."""
        while not self._stop_event.is_set():
            try:
                data_point = self._collect_data_point()
                if data_point:
                    data_point['timestamp'] = time.time() # Add a timestamp for each sample
                    self._data_points.append(data_point)
            except Exception as e:
                print(f"Error collecting {self.name} data: {e}")
            finally:
                # Sleep for the interval, but allow the stop event to interrupt quickly
                self._stop_event.wait(self.interval)

    def start(self):
        """Starts the continuous data collection in a separate thread."""
        if self._is_running:
            print(f"  {self.name} collector is already running.")
            return

        self._data_points = []  # Clear previous data points for a new collection run
        self._stop_event.clear() # Clear the stop signal
        self._thread = threading.Thread(target=self._run_collection, daemon=True) # Daemon thread exits with main program
        self._thread.start()
        self._is_running = True
        print(f"  {self.name} collector started.")

    def stop(self) -> list[dict]:
        """
        Stops the data collection thread and returns all raw collected data points.
        """
        if not self._is_running:
            print(f"  {self.name} collector is not running.")
            return []

        self._stop_event.set() # Signal the thread to stop
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self.interval * 2 + 1) # Wait for thread to finish, with a timeout
            if self._thread.is_alive():
                print(f"  Warning: {self.name} collector thread did not stop gracefully.")
        
        self._is_running = False
        print(f"  {self.name} collector stopped. Collected {len(self._data_points)} data points.")
        return self._data_points

    def get_summary(self) -> dict:
        """
        Processes the collected raw data points and returns a summary.
        This method can be overridden by subclasses for more specific summaries.
        """
        if not self._data_points:
            return {}

        df = pd.DataFrame(self._data_points)
        summary = {}

        for col in df.columns:
            if col != 'timestamp' and pd.api.types.is_numeric_dtype(df[col]):
                # Add '_eval_avg' and '_eval_max' suffix to distinguish from LLM metrics
                summary[f"{col}_eval_avg"] = df[col].mean()
                summary[f"{col}_eval_max"] = df[col].max()
                # Consider adding other stats like min, p90, std dev if useful for analysis
                # summary[f"{col}_eval_min"] = df[col].min()
                # summary[f"{col}_eval_p90"] = df[col].quantile(0.9)
        return summary