# LLMInsight/data_collection/ollama_client.py
import ollama
import time

class OllamaClient:
    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.model = model
        self.client = ollama.Client(host=host)

    def check_model_exists(self):
        """Checks if the specified model is available locally."""
        try:
            # This will raise a ResponseError if the model is not found
            self.client.show(self.model)
            return True
        except ollama.ResponseError as e:
            if e.status_code == 404:
                raise ValueError(f"Model '{self.model}' not found. Please pull it first.")
            else:
                raise ConnectionError(f"Failed to connect to Ollama server: {e}")
        except Exception as e:
            raise ConnectionError(f"An unexpected error occurred when checking model: {e}")

    def chat(self, prompt: str, options: dict = None) -> tuple:
        """
        Sends a chat prompt to Ollama and collects timing data.
        Returns: (full_response_content, total_duration, first_token_latency, tokens_generated)
        """
        if options is None:
            options = {}

        full_response_content = ""
        tokens_generated = 0
        first_token_time = None

        start_time = time.time()
        try:
            response_stream = self.client.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options=options,
                stream=True # Always stream to measure first token and tokens/second
            )

            for chunk in response_stream:
                if not first_token_time:
                    first_token_time = time.time() # Mark time when first token is received
                content = chunk['message']['content']
                full_response_content += content
                # Simple token count: assumes each chunk is one token.
                # For better accuracy, use a proper tokenizer (e.g., tiktoken for GPT-like models, but for Ollama it's less straightforward).
                tokens_generated += 1 

        except ollama.ResponseError as e:
            print(f"Ollama Response Error: {e.status_code} - {e.error}")
            raise e
        except Exception as e:
            print(f"An unexpected error during Ollama chat: {e}")
            raise e

        end_time = time.time()

        total_duration = end_time - start_time
        first_token_latency = first_token_time - start_time if first_token_time else total_duration # Fallback if no tokens

        return full_response_content, total_duration, first_token_latency, tokens_generated