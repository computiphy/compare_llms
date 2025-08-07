from abc import ABC, abstractmethod
import pandas as pd

class ComparisonMethod(ABC):
    """
    Abstract base class for all comparison methods.
    Each comparison method should inherit from this class and implement
    the 'compare' method.
    """
    def __init__(self, name: str, description: str):
        """Initialize a new instance of the class with a given name and description.

    Parameters:
    - name (str): The name of the entity.
    - description (str): A brief description or purpose of the entity."""
        self.name = name
        self.description = description

    @abstractmethod
    def compare(self, data: pd.DataFrame, features: list, output_dir: str) -> dict:
        """
        Performs the comparison and analysis for a specific method.

        Args:
            data (pd.DataFrame): The raw experiment results collected from LLM runs.
                                 This DataFrame should contain columns like 'model',
                                 'prompt', 'iteration', 'generated_text', and various metrics.
            features (list): A list of feature/metric names (strings) that are
                             relevant to this comparison method.
            output_dir (str): The directory where any method-specific outputs (e.g., plots,
                              intermediate files) should be saved.

        Returns:
            dict: A dictionary containing results to be included in the HTML report.
                  Expected keys:
                  - 'aggregated_data': (Optional) A pandas DataFrame or string representing
                                       aggregated data to display in a table.
                  - 'plots': (Optional) A dictionary where keys are plot titles (str)
                             and values are matplotlib Figure objects.
                  - 'sample_outputs': (Optional) A dictionary where keys are prompts (str)
                                      and values are generated texts (str) for qualitative review.
        """
        pass