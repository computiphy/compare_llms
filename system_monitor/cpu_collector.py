# system_monitor/cpu_collector.py
import psutil
from .base_metric_collector import BaseMetricCollector

class CPUCollector(BaseMetricCollector):
    """This class collects CPU-related metrics, including CPU usage, system-wide load averages,
    and optionally CPU temperatures. It uses the `psutil` library to retrieve these statistics.

    Attributes:
        interval (float): The time interval in seconds between data collection attempts.
        
    Methods:
        _collect_data_point() -> dict: Collects current CPU percentage and normalized load averages.
                                     Optionally, it retrieves and normalizes CPU temperatures if supported by psutil."""
    def __init__(self, interval: float = 0.5):
        """Initialize a CPU monitoring object with the given polling interval.

    Parameters:
    - interval (float): The time interval in seconds between each CPU usage measurement.
      Default is 0.5 seconds.

    Initializes the parent class 'CPU Monitor' with its name and the specified interval,
    and ensures that psutil can make non-blocking calls to retrieve the CPU percentage."""
        super().__init__("CPU Monitor", interval)
        # Prime psutil for non-blocking cpu_percent calls
        psutil.cpu_percent(interval=None) 

    def _collect_data_point(self) -> dict:
        """Collect and return a dictionary containing system resource metrics.

    The returned dictionary includes the following keys:
        - 'cpu_percent': Current CPU usage percentage.
        - 'load_avg_1min_normalized': Load average for the past minute normalized by the number of CPU cores.
        - 'load_avg_5min_normalized': Load average for the past five minutes normalized by the number of CPU cores.
        - 'load_avg_15min_normalized': Load average for the past fifteen minutes normalized by the number of CPU cores.

    Note: This function may not be available or return CPU temperature on all systems. For more detailed data, consider using additional libraries or APIs."""
        data = {
            "cpu_percent": psutil.cpu_percent(interval=None) # Non-blocking call for current usage since last call
        }
        # Load average is system-wide and typically for 1, 5, 15 minutes
        load_avg = psutil.getloadavg()
        if load_avg:
            # Normalize load average by number of CPU cores for a more comparable metric
            num_cores = psutil.cpu_count(logical=True)
            data["load_avg_1min_normalized"] = load_avg[0] / num_cores
            data["load_avg_5min_normalized"] = load_avg[1] / num_cores
            data["load_avg_15min_normalized"] = load_avg[2] / num_cores
        
        # Add CPU temperature (if available and supported by psutil)
        # psutil.sensors_temperatures() might not be available or return CPU temp on all systems
        # temps = psutil.sensors_temperatures()
        # if 'coretemp' in temps and temps['coretemp']: # Common for Intel/AMD CPUs
        #     cpu_temps = [t.current for t in temps['coretemp']]
        #     data["cpu_temp_celsius_avg"] = sum(cpu_temps) / len(cpu_temps) if cpu_temps else np.nan
        #     data["cpu_temp_celsius_max"] = max(cpu_temps) if cpu_temps else np.nan
        # elif 'cpu_thermal' in temps and temps['cpu_thermal']: # Another common key
        #     cpu_temps = [t.current for t in temps['cpu_thermal']]
        #     data["cpu_temp_celsius_avg"] = sum(cpu_temps) / len(cpu_temps) if cpu_temps else np.nan
        #     data["cpu_temp_celsius_max"] = max(cpu_temps) if cpu_temps else np.nan
        
        return data