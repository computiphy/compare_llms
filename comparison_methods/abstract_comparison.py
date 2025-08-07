# comparison_methods/abstract_comparison.py
from abc import ABC, abstractmethod
import pandas as pd

class ComparisonMethod(ABC):
    """self.name = name
        self.description = description

    @abstractmethod
    def visualize(self, data: pd.DataFrame, feature_name: str, metric_name: str, title: str, output_path: str):
    
        Visualizes the data using the specific comparison method.
        
        :param data: DataFrame containing experiment results.
        :param feature_name: Column name for the LLM feature being varied (X-axis).
        :param metric_name: Column name for the metric being plotted (Y-axis).
        :param title: Title for the visualization.
        :param output_path: Path to save the generated plot/table.
        """
    def __init__(self, name: str, description: str):
        """Initializes the object with `name` and `description`.

Parameters:
- name (str): A brief identifier or title for the object.
- description (str): A detailed explanation or description of the object's purpose or functionality.

Attributes:
- self.name: The identifier or title of the object.
- self.description: The description of the object's purpose or functionality."""
        self.name = name
        self.description = description

    @abstractmethod
    def visualize(self, data: pd.DataFrame, feature_name: str, metric_name: str, title: str, output_path: str):
        """
        Visualizes the data using the specific comparison method.
        :param data: DataFrame containing experiment results.
        :param feature_name: Column name for the LLM feature being varied (X-axis).
        :param metric_name: Column name for the metric being plotted (Y-axis).
        :param title: Title for the visualization.
        :param output_path: Path to save the generated plot/table.
        """
        pass