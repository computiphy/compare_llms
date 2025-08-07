# system_monitor/gpu_collector.py
from .base_metric_collector import BaseMetricCollector
import numpy as np

_pynvml_available = False
try:
    from pynvml.nvml import *  # Import all NVML constants and functions
    _pynvml_available = True
except ImportError:
    print("Warning: pynvml library not found. GPU metrics will not be collected. Install with 'pip install pynvml'.")
except Exception as error:
    print(f"Warning: NVML initialization failed or not found ({error}). GPU metrics will not be collected. Ensure NVIDIA drivers are installed and NVML is accessible.")


class GPUCollector(BaseMetricCollector):
    """A class for collecting GPU metrics using the PyNVML library. This collector queries NVIDIA GPUs to retrieve utilization, memory usage,
    temperature, and power consumption data at a specified interval.

    Args:
        interval (float): The time interval in seconds between each collection of data points.
                         Default is 0.5 seconds.

    Attributes:
        _gpu_count (int): The number of detected NVIDIA GPUs.
        _pynvml_available (bool): Flag indicating if PyNVML is available and correctly initialized.

    Methods:
        __init__: Initializes the GPUCollector with a given interval and checks for NVIDIA GPU support.
        _collect_data_point: Collects metrics from each connected NVIDIA GPU at the current time point.
        stop: Stops data collection and shuts down NVML if it was previously initialized."""
    def __init__(self, interval: float = 0.5):
        """Initialize the GPU Monitor with the specified collection interval (default is 0.5 seconds).

    If NVML is available and initialized successfully, it retrieves the number of NVIDIA GPUs.
    It also prints a message indicating whether any GPUs were detected or not.

    Parameters:
        interval (float): The time interval between each data collection in seconds.

    Note:
        - NVML must be installed to use this functionality.
        - If NVML initialization fails, GPU metrics collection will be disabled."""
        global _pynvml_available  # Declare global before using/assigning

        super().__init__("GPU Monitor", interval)
        self._gpu_count = 0

        if _pynvml_available:
            try:
                nvmlInit()  # Initialize NVML library
                self._gpu_count = nvmlDeviceGetCount()
                if self._gpu_count > 0:
                    print(f"  Detected {self._gpu_count} NVIDIA GPU(s).")
                else:
                    print("  No NVIDIA GPUs detected.")
                    _pynvml_available = False
            except NVMLError as error:
                print(f"Warning: NVML initialization or device count failed: {error}. GPU metrics will not be collected.")
                _pynvml_available = False

    def _collect_data_point(self) -> dict:
        """Collects data points for GPU metrics such as utilization, memory usage, temperature, and power consumption.

    This function retrieves information from NVIDIA Management Library (NVML) to gather details about each GPU in the system.
    It handles errors gracefully by skipping GPUs that cannot be accessed or are not available.

    Returns:
        A dictionary containing GPU-specific data points. Each key is formatted as 'gpu_<index>_<metric>' where
        <index> corresponds to the GPU index and <metric> is one of: utilization_percent, memory_utilization_percent,
        memory_used_gb, memory_total_gb, memory_free_gb, temperature_celsius, or power_watts."""
        if not _pynvml_available or self._gpu_count == 0:
            return {}

        gpu_data = {}
        gb_divisor = 1024**3  # Convert bytes to GB

        for i in range(self._gpu_count):
            try:
                handle = nvmlDeviceGetHandleByIndex(i)

                # Utilization
                utilization = nvmlDeviceGetUtilizationRates(handle)
                gpu_data[f"gpu_{i}_utilization_percent"] = utilization.gpu
                gpu_data[f"gpu_{i}_memory_utilization_percent"] = utilization.memory  # Memory controller utilization

                # Memory Info
                mem_info = nvmlDeviceGetMemoryInfo(handle)
                gpu_data[f"gpu_{i}_memory_used_gb"] = mem_info.used / gb_divisor
                gpu_data[f"gpu_{i}_memory_total_gb"] = mem_info.total / gb_divisor
                gpu_data[f"gpu_{i}_memory_free_gb"] = mem_info.free / gb_divisor

                # Temperature
                temperature = nvmlDeviceGetTemperature(handle, NVML_TEMP_GPU)
                gpu_data[f"gpu_{i}_temperature_celsius"] = temperature

                # Power Usage
                if hasattr(nvmlDeviceGetPowerUsage, '__call__'):
                    power_usage = nvmlDeviceGetPowerUsage(handle)
                    gpu_data[f"gpu_{i}_power_watts"] = power_usage / 1000.0  # Convert mW to W

            except NVMLError as error:
                print(f"Error collecting data for GPU {i}: {error}. Skipping this GPU's metrics for this sample.")
                # Fill with NaN for missing data
                gpu_data[f"gpu_{i}_utilization_percent"] = np.nan
                gpu_data[f"gpu_{i}_memory_utilization_percent"] = np.nan
                gpu_data[f"gpu_{i}_memory_used_gb"] = np.nan
                gpu_data[f"gpu_{i}_memory_total_gb"] = np.nan
                gpu_data[f"gpu_{i}_memory_free_gb"] = np.nan
                gpu_data[f"gpu_{i}_temperature_celsius"] = np.nan
                gpu_data[f"gpu_{i}_power_watts"] = np.nan
                continue

        return gpu_data

    def stop(self) -> list[dict]:
        """Stops the current operation and shuts down the NVIDIA Management Library (NVML).
    
    Returns:
        A list of dictionaries containing the results of any previously collected data.
        
    Raises:
        NVMLError: If there is an error shutting down NVML."""
        collected_data = super().stop()
        if _pynvml_available:
            try:
                nvmlShutdown()
                print("  NVML shut down.")
            except NVMLError as error:
                print(f"Error shutting down NVML: {error}")
        return collected_data
