# LLMInsight/features/system_params.py
from .abstract_feature import LLMFeature

# NOTE: Comparing these parameters effectively requires setting up
# different Modelfiles for your Ollama models and running comparisons
# between these distinct model versions (e.g., llama2-mmap-true vs llama2-mmap-false).
# The main.py currently skips dynamic API calls for these.

class UseMmap(LLMFeature):
    """Class to control whether to use memory mapping for loading models.
    
    Attributes:
        name (str): The name of the feature ("UseMmap").
        description (str): A description of the feature and its purpose ("Whether to use mmap for model loading (performance/memory).").
        category (str): The category of the feature in Ollama ("system").

    Methods:
        get_ollama_param_name() -> str: Returns the name of the parameter used in the Modelfile.
        get_test_values() -> list: Returns a list of boolean values to test, indicating whether to use mmap for model loading."""
    def __init__(self):
        """
    Initializes a new instance of the class with specific parameters related to GPU layer offloading.

    Parameters:
        device_type (str): The type of device for offloading, in this case 'NumGpu'.
        description (str): A description of what the parameter represents.
        category (str): The category or scope of the parameter, in this case 'system'.

    Returns:
        None
    """
    def __init__(self):
        super().__init__("NumGpu", "Number of GPU layers to offload to the GPU.", "system")

    def get_ollama_param_name(self) -> str:
        """Returns the parameter name used in the Ollama model file.
    
    This method returns 'num_gpu', which is a configuration parameter that specifies the number of GPUs to use when running an AI model. The value returned by this function is commonly referenced in the Modelfile used with the Ollama AI platform for training and inference tasks."""
        return "use_mmap" # Used in Modelfile
    def get_test_values(self) -> list:
        """Retrieves the test values for a specific configuration.

    Returns:
        list: A list containing two values. The first value is determined by the GPU and model size, with 0 indicating CPU-only use.
              The second value is often set to 99, which may represent "all layers possible" or a similar concept depending on context."""
        return [True, False] # Boolean values

class UseMlock(LLMFeature):
    """A feature to control whether the model is locked into RAM (preventing swapping).

    Attributes:
        - name: "UseMlock"
          description: Whether to lock model into RAM.
          category: system

    Methods:
        - get_ollama_param_name() -> str
            Returns the parameter name used in Modelfile, which is "use_mlock".
        
        - get_test_values() -> list
            Provides test values for use in testing, including [True, False]."""
    def __init__(self):
        """
    Initializes a new instance of the class with specific parameters related to GPU layer offloading.

    Parameters:
        device_type (str): The type of device for offloading, in this case 'NumGpu'.
        description (str): A description of what the parameter represents.
        category (str): The category or scope of the parameter, in this case 'system'.

    Returns:
        None
    """
    def __init__(self):
        super().__init__("NumGpu", "Number of GPU layers to offload to the GPU.", "system")
        
    def get_ollama_param_name(self) -> str:
        """Returns the parameter name used in the Ollama model file.
    
    This method returns 'num_gpu', which is a configuration parameter that specifies the number of GPUs to use when running an AI model. The value returned by this function is commonly referenced in the Modelfile used with the Ollama AI platform for training and inference tasks."""
        return "use_mlock" # Used in Modelfile
    def get_test_values(self) -> list:
        """Retrieves the test values for a specific configuration.

    Returns:
        list: A list containing two values. The first value is determined by the GPU and model size, with 0 indicating CPU-only use.
              The second value is often set to 99, which may represent "all layers possible" or a similar concept depending on context."""
        return [True, False]

class NumThread(LLMFeature):
    """A class representing the number of threads to use for computation.

    Attributes:
    - model_name (str): The name of the LLM feature.
    - description (str): A description of the LLM feature and its purpose.
    - category (str): The category of the LLM feature, typically 'system'.
    
    Methods:
    - get_ollama_param_name() -> str: Returns the Ollama parameter name for the number of threads.
    - get_test_values() -> list: Returns a list of example thread counts to test."""
    def __init__(self):
        """
    Initializes a new instance of the class with specific parameters related to GPU layer offloading.

    Parameters:
        device_type (str): The type of device for offloading, in this case 'NumGpu'.
        description (str): A description of what the parameter represents.
        category (str): The category or scope of the parameter, in this case 'system'.

    Returns:
        None
    """
    def __init__(self):
        super().__init__("NumGpu", "Number of GPU layers to offload to the GPU.", "system")

    def get_ollama_param_name(self) -> str:
        """Returns the parameter name used in the Ollama model file.
    
    This method returns 'num_gpu', which is a configuration parameter that specifies the number of GPUs to use when running an AI model. The value returned by this function is commonly referenced in the Modelfile used with the Ollama AI platform for training and inference tasks."""
        return "num_thread" # Used in Modelfile
    def get_test_values(self) -> list:
        """Retrieves the test values for a specific configuration.

    Returns:
        list: A list containing two values. The first value is determined by the GPU and model size, with 0 indicating CPU-only use.
              The second value is often set to 99, which may represent "all layers possible" or a similar concept depending on context."""
        return [1, 4, 8] # Example thread counts

class NumGpu(LLMFeature):
    """Represents the configuration for offloading a certain number of layers to the GPU.

    Attributes:
        name (str): The name of the feature, typically 'NumGpu'.
        description (str): A brief description of the feature, explaining its purpose and usage.
        category (str): The category of the feature, likely 'system'.

    Methods:
        get_ollama_param_name() -> str: Returns the parameter name used in the Ollama configuration file for this feature.
        get_test_values() -> list: Provides a list of test values to evaluate this feature's performance and effectiveness. These values can vary based on the GPU capabilities and model size, with 99 often representing "all layers possible."""
    def __init__(self):
        """
    Initializes a new instance of the class with specific parameters related to GPU layer offloading.

    Parameters:
        device_type (str): The type of device for offloading, in this case 'NumGpu'.
        description (str): A description of what the parameter represents.
        category (str): The category or scope of the parameter, in this case 'system'.

    Returns:
        None
    """
    def __init__(self):
        super().__init__("NumGpu", "Number of GPU layers to offload to the GPU.", "system")

    def get_ollama_param_name(self) -> str:
        """Returns the parameter name used in the Ollama model file.
    
    This method returns 'num_gpu', which is a configuration parameter that specifies the number of GPUs to use when running an AI model. The value returned by this function is commonly referenced in the Modelfile used with the Ollama AI platform for training and inference tasks."""
        return "num_gpu" # Used in Modelfile
    def get_test_values(self) -> list:
        """Retrieves the test values for a specific configuration.

    Returns:
        list: A list containing two values. The first value is determined by the GPU and model size, with 0 indicating CPU-only use.
              The second value is often set to 99, which may represent "all layers possible" or a similar concept depending on context."""
        # This depends heavily on your GPU and model size. 0 means CPU only.
        return [0, 99] # 99 often means "all layers possible"