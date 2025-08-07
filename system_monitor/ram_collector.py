# system_monitor/ram_collector.py
import psutil
from .base_metric_collector import BaseMetricCollector

class RAMCollector(BaseMetricCollector):
    """A class for collecting and reporting real-time RAM usage statistics.

    This collector periodically retrieves memory usage metrics from the system using the `psutil` library
    and reports them as a dictionary containing total, available, used, and percentage of RAM in gigabytes.
    
    Attributes:
        - interval (float): The time interval in seconds between data collection cycles.
        
    Methods:
        - _collect_data_point(): Collects and returns memory usage statistics in gigabytes."""
    def __init__(self, interval: float = 0.5):
        """Initialize the RAM Monitor with a default interval of 0.5 seconds.

    Parameters:
    - interval (float): The time interval in seconds between updates. Defaults to 0.5 seconds."""
        super().__init__("RAM Monitor", interval)

    def _collect_data_point(self) -> dict:
        """Collects and returns system RAM usage metrics in gigabytes.

    Returns:
        A dictionary containing the following keys:
        - 'total_ram_gb': Total available memory in gigabytes.
        - 'available_ram_gb': Free memory in gigabytes.
        - 'used_ram_gb': Memory currently used in gigabytes.
        - 'ram_percent': Percentage of RAM that is being used.

    This function uses the `psutil` library to retrieve system memory information and
    formats it into gigabyte units for easier readability."""
        mem = psutil.virtual_memory()
        gb_divisor = (1024**3) # Convert bytes to GB
        return {
            "total_ram_gb": mem.total / gb_divisor,
            "available_ram_gb": mem.available / gb_divisor,
            "used_ram_gb": mem.used / gb_divisor,
            "ram_percent": mem.percent
        }