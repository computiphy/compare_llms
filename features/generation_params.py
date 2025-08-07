# features/generation_params.py
from .abstract_feature import LLMFeature

class Temperature(LLMFeature):
    """Controls the randomness of the output.

    Attributes:
        name (str): The feature's name.
        description (str): A brief description of the feature and its purpose.
        category (str): The category to which this feature belongs.

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name associated with this feature.
        get_test_values() -> list: Provides a list of test values for this feature."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("Temperature", "Controls the randomness of the output.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "temperature"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0.0, 0.2, 0.5, 0.8, 1.0] # Common temperature values

class TopK(LLMFeature):
    """
    A class to handle the 'TopK' LLM feature.

    This class is designed to limit the vocabulary for token selection to the top K tokens.
    It provides functionality to retrieve the Ollama parameter name and test values for this feature.

    Attributes:
        name (str): The name of the feature, which is "TopK".
        description (str): A brief description of the feature, specifying that it limits
                         token selection to the top K tokens.
        category (str): The category of the feature, which is "generation".
    """
    
    def __init__(self):
        super().__init__("TopK", "Limits the vocabulary for token selection to the top K tokens.", "generation")
    
    def get_ollama_param_name(self) -> str:
        """
        Returns the Ollama parameter name associated with this feature.

        This method returns 'top_k', which is the Ollama parameter used to specify
        the number of top tokens to consider for selection in token generation.
        
        :return: The Ollama parameter name as a string.
        :rtype: str
        """
        return "top_k"
    
    def get_test_values(self) -> list:
        """
        Returns a list of test values for the 'TopK' feature.

        This method returns a list of integers representing different levels of K, where 0 means
        that token selection is not limited to any specific number of top tokens. The list includes
        common values like 20 and 40, as well as an example of the model's default behavior (80).

        :return: A list of test values for the 'TopK' feature.
        :rtype: list[int]
        """
        return [0, 20, 40, 80]  # 0 means disabled (or model default)"""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("TopK", "Limits the vocabulary for token selection to the top K tokens.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "top_k"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0, 20, 40, 80] # 0 means disabled (or model default)

class TopP(LLMFeature):
    """Implements the 'TopP' strategy for controlling text generation in LLMs.

    This feature selects the smallest set of tokens whose cumulative probability exceeds a specified threshold (p).
    A value of 1.0 includes all tokens, while 0.0 disables it (or uses model default).

    Parameters:
    - name: The name of the feature.
    - description: A brief description of how the feature works.
    - category: The category this feature belongs to in the LLM generation process.

    Methods:
    - get_ollama_param_name(): Returns the OLLAMA-specific parameter name for TopP.
    - get_test_values(): Provides a list of test values for TopP, including 0.0 (disabled), 0.5, 0.9, and 1.0 (includes all tokens)."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("TopP", "Selects the smallest set of tokens whose cumulative probability exceeds P.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "top_p"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0.0, 0.5, 0.9, 1.0] # 0.0 means disabled (or model default), 1.0 includes all tokens

class MinP(LLMFeature):
    """Class to configure the minimum probability for a token to be considered in text generation.

    Attributes:
        name (str): The name of the configuration parameter, "MinP".
        description (str): A brief description of the purpose and use of this configuration, "Sets the minimum probability for a token to be considered."
        category (str): The category or type of configuration, "generation".

    Methods:
        get_ollama_param_name() -> str: Returns the name of the Ollama parameter associated with this configuration.
        get_test_values() -> list: Provides a list of test values to verify and validate the configuration."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("MinP", "Sets the minimum probability for a token to be considered.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "min_p"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0.0, 0.05, 0.1]

class RepeatLastN(LLMFeature):
    """
    Sets the model's ability to repeat the last N tokens. 
    This feature helps prevent repetitive outputs by restricting the context length.
    
    Parameters:
    - repeat_last_n (int): The number of tokens to look back in the generated text for repetition prevention. Setting it to 0 disables this feature.

    Test Values:
    - [0, 32, 64]: 
      - 0: Disables repetition prevention
      - 32: Limits the context length to the last 32 tokens
      - 64: Limits the context length to the last 64 tokens
    """

    def __init__(self):
        super().__init__("RepeatLastN", "Sets how far back for the model to look to prevent repetition.", "generation")
    
    def get_ollama_param_name(self) -> str:
        return "repeat_last_n"
    
    def get_test_values(self) -> list:
        return [0, 32, 64] # 0 for disabled"""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("RepeatLastN", "Sets how far back for the model to look to prevent repetition.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "repeat_last_n"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0, 32, 64] # 0 for disabled

class FrequencyPenalty(LLMFeature):
    """Class for implementing the Frequency Penalty feature in LLMs.
    
    This class penalizes new tokens based on their existing frequency in the text so far,
    encouraging diverse and less repetitive generation of responses.

    Attributes:
        name (str): The name of the feature, "FrequencyPenalty".
        description (str): A detailed description of the feature's purpose and effect.
        category (str): The category to which this feature belongs, "generation".

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name for this feature.
        get_test_values() -> list: Provides a list of test values for the Frequency Penalty, ranging from 0.0 to 1.0."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("FrequencyPenalty", "Penalizes new tokens based on their existing frequency in the text so far.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "frequency_penalty"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0.0, 0.1, 0.5, 1.0]

class TfsZ(LLMFeature):
    """TfsZ feature for LLMs.

    Attributes:
    - name: "TfsZ"
    - description: "Tail Free Sampling parameter. Higher values reduce the impact of less probable tokens."
    - category: "generation"

    Methods:
    - get_ollama_param_name(): Returns "tfs_z".
    - get_test_values(): Returns a list of test values for TFS-Z, including 0.0, 0.5, and 1.0."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("TfsZ", "Tail Free Sampling parameter. Higher values reduce the impact of less probable tokens.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "tfs_z"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0.0, 0.5, 1.0]

# Note: Context Length (num_ctx), Batch Size (num_batch), Max Tokens (num_predict)
# These are usually in Modelfiles or advanced options. For now, treat them as generation,
# but be aware of their typical usage in Ollama.
class ContextLength(LLMFeature):
    """
    A class to represent and manage context length settings for an LLM.

    Attributes:
        name (str): The name of the feature.
        description (str): A brief description of the feature's purpose.
        type (str): The type of the feature, indicating its use in generation tasks.

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name for context length.
        get_test_values() -> list: Provides test values for context length to ensure optimal performance and resource management. Be cautious with high values as they may consume more RAM.

This docstring provides a clear overview of the `ContextLength` class, including its attributes, methods, and their purposes. The description explains the role of this feature in LLM generation tasks and mentions typical usage scenarios for Ollama."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("ContextLength", "Sets the size of the context window.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "num_ctx"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        # Be careful with high values, they consume more RAM
        return [512, 1024, 2048] 

class BatchSize(LLMFeature):
    """A class representing the configuration of batch size for prompt processing.

    Attributes:
        name (str): The name of the feature.
        description (str): A brief description of the feature's purpose.
        category (str): The category to which this feature belongs, typically 'generation'.

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name for batch size configuration.
        get_test_values() -> list: Returns a list of test values for batch size, suitable for typical use cases."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("BatchSize", "Sets the batch size for prompt processing.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "num_batch"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [1, 4, 8] # Small batches for typical use cases

class MaxTokens(LLMFeature):
    """Represents a feature that sets the maximum number of tokens to predict in an LLM response.

    Attributes:
    - name (str): The name of the feature as "MaxTokens".
    - description (str): A brief description of the feature and its purpose, which is "Sets the maximum number of tokens to predict."
    - category (str): The category of this feature, which is "generation".

    Methods:
    - get_ollama_param_name() -> str: Returns the Ollama parameter name associated with setting the maximum number of tokens.
    - get_test_values() -> list: Provides a list of test values for validation and benchmarking, including 64, 128, and 256 tokens."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("MaxTokens", "Sets the maximum number of tokens to predict.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "num_predict"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [64, 128, 256]

# TODO: Mirostat, Mirostat Eta, Mirostat Tau
# Mirostat can be 0 (disabled), 1 (Mirostat), 2 (Mirostat 2.0)
class Mirostat(LLMFeature):
    """Mirostat is a method for controlling the perplexity of generated text using a learned model.

    Parameters:
        name (str): The name of the feature.
        description (str): A brief description of the feature's purpose and its role in text generation.
        category (str): The category to which this feature belongs, typically "generation".

    Attributes:
        ollama_param_name (str): The OLLAMA parameter name for Mirostat control.

    Methods:
        get_ollama_param_name() -> str: Returns the OLLAMA parameter name for Mirostat.
        get_test_values() -> list: Provides test values for the Mirostat feature, including disabled, Mirostat, and Mirostat 2.0 modes."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("Mirostat", "Enables Mirostat sampling for perplexity control.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "mirostat"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0, 1, 2] # 0=disabled, 1=mirostat, 2=mirostat_v2

class MirostatEta(LLMFeature):
    """MirostatEta class for setting the learning rate in the Mirostat algorithm.

    Attributes:
        name (str): The name of the feature.
        description (str): A brief description of the feature's purpose and use.
        data_type (str): The type of data that this feature can handle, typically 'generation'.

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name associated with MirostatEta.
        get_test_values() -> list: Returns a list of test values for the learning rate."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("MirostatEta", "Learning rate for Mirostat algorithm.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "mirostat_eta"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [0.01, 0.1, 0.2] # Default 0.1

class MirostatTau(LLMFeature):
    """Represents the Mirostat Tau value used in the Mirostat algorithm for controlling token sampling and perplexity.

    Attributes:
        name (str): The name of the feature.
        description (str): A brief description of the Mirostat Tau parameter.
        category (str): The category under which this feature falls, such as "generation".

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name associated with this feature.
        get_test_values() -> list: Returns a list of default test values for Mirostat Tau."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("MirostatTau", "Target perplexity for Mirostat algorithm.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "mirostat_tau"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        return [3.0, 5.0, 8.0] # Default 5.0

class StreamChatResponse(LLMFeature):
    """Determines if the response from the Ollama LLM service should be streamed token by token.

    This feature simulates streaming behavior for comparison purposes, using `stream=True`.
    It measures metrics such as first_token_latency during streaming to evaluate its impact on performance.
    
    For direct comparisons (stream=True vs stream=False), you would need to modify the Ollama client's
    `chat` method to handle these cases separately.

    Attributes:
        name (str): The name of the feature, "StreamChatResponse".
        description (str): A brief description of the feature, "Determines if response is streamed token by token."
        category (str): The category of the feature, "generation".

    Methods:
        get_ollama_param_name() -> str: Returns a dummy name for identification purposes.
        get_test_values() -> list: Provides test values for streaming, including stream=True."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        # This feature is more about the Ollama client's `stream` parameter,
        # which affects how we process the response (chunk by chunk vs. full).
        # The 'options' dict itself doesn't typically have a 'stream' key.
        # However, for comparison purposes, we can simulate its effect by
        # always using stream=True and measuring first_token_latency, etc.
        # For direct comparison of 'stream=True' vs 'stream=False', you'd need
        # to modify the ollama_client.chat() behavior based on this 'feature'.
        super().__init__("StreamChatResponse", "Determines if response is streamed token by token.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        # This is not a direct 'option' parameter, it controls the API call itself.
        # We'll use a dummy name and handle its logic in ollama_client.py if needed.
        return "stream_chat_response_internal_flag" # Dummy name for identification
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        # You can represent this as a boolean or just focus on the metrics derived
        # from streaming (first_token_latency). If you wanted to test non-streaming,
        # you'd need to modify the ollama_client.chat() to call with stream=False.
        # For this initial setup, we measure streaming benefits by default with stream=True.
        return [True] # We assume streaming is always on for metric collection.
                      # To truly compare (stream=True vs stream=False),
                      # you'd need a more complex client.chat wrapper.


class Seed(LLMFeature):
    """Class for setting the random seed for reproducibility.

    Attributes:
    - name (str): The name of the feature.
    - description (str): A brief description of the feature and its purpose.
    - category (str): The category or topic associated with this feature.

    Methods:
    - __init__(): Initializes the Seed class with a name, description, and category.
    - get_ollama_param_name() -> str: Returns the parameter name used in Ollama to set the seed.
    - get_test_values() -> list: Provides test values for comparing different seeds on generation variance."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("Seed", "Sets the random seed for reproducibility.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "seed"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        # You wouldn't typically compare different seeds, but fix one
        # or compare a few to show impact on generation variance.
        return [0, 42, 123] # Test impact of different seeds on diversity metrics

class StopSequence(LLMFeature):
    """A class that represents a list of strings used to stop text generation.

    Attributes:
        name (str): The name of the feature, 'StopSequence'.
        description (str): A brief description of what the feature does.
        type (str): The category or purpose of the feature, "generation".

    Methods:
        get_ollama_param_name() -> str: Returns the Ollama parameter name for this feature.
        get_test_values() -> list: Provides test values for validation and examples of how to use this feature. Includes cases without stops, single stop sequences, and multiple stop sequences."""
    def __init__(self):
        """Initialize the StopSequence object with default parameters.

    This method initializes a new instance of the StopSequence class, which is designed to manage a list of strings that should be used as stop signals for text generation. The `name` parameter sets the name of this component, "StopSequence", and it describes the purpose of this component as a list of strings intended to halt the generation process once encountered. The `scope` parameter indicates that this component is primarily associated with the generation task."""
        super().__init__("StopSequence", "A list of strings to stop generation at.", "generation")
    def get_ollama_param_name(self) -> str:
        """Returns the Ollama parameter name for stopping text generation.
    
    This function is specifically designed to return the string 'stop' which is used as an argument in the Ollama API for specifying the termination criteria of text generation."""
        return "stop"
    def get_test_values(self) -> list:
        """Returns a list of test values representing different scenarios for handling stop sequences in text processing.
    
    Each element in the returned list contains a sequence that can be used to identify and process stops within a text string.
    - The first value is `None`, indicating no explicit stop sequences are present.
    - The second value, `["\n"]`, represents a newline character as the only stop sequence.
    - The third value, `["\n", "."]`, indicates both a newline and a period as potential stop sequences.
    
    This function is useful for testing various text processing algorithms that need to identify and handle different types of delimiters."""
        # Example: comparing no stop, single stop, multiple stops
        return [None, ["\n"], ["\n", "."]] # None means no explicit stop sequences