# LLMInsight/features/abstract_feature.py
from abc import ABC, abstractmethod

class LLMFeature(ABC):
    """Abstract base class representing an LLM (Large Language Model) feature.

    Attributes:
    - name: A string representing the name of the feature.
    - description: A string describing what the feature does.
    - param_type: A string indicating the type of parameter this feature represents,
                 typically 'generation' for generation-related parameters or 'system'
                 for system parameters.

    Methods:
    - get_ollama_param_name() -> str:
        Returns the Ollama API option name associated with this feature.
        This is used in the configuration files and API requests.

    - get_test_values() -> list:
        Provides a set of values to be tested for this LLM feature.
        These values are useful for validation and testing purposes."""
    def __init__(self, name: str, description: str, param_type: str):
        """Initialize the instance with the provided parameters.

    Parameters:
    - name (str): The unique identifier for the parameter.
    - description (str): A brief description of what the parameter is used for.
    - param_type (str): The type of parameter ("generation" or "system")."""
        self.name = name
        self.description = description
        self.param_type = param_type # e.g., "generation", "system"

    @abstractmethod
    def get_ollama_param_name(self) -> str:
        """Returns the parameter name used in Ollama API options (e.g., 'temperature')
           or the Modelfile parameter name (e.g., 'num_gpu')."""
        pass

    @abstractmethod
    def get_test_values(self) -> list:
        """Returns a list of values to test for this feature."""
        pass