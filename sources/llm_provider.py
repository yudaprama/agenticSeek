import httpx
from ollama import Client as OllamaClient

from sources.logger import Logger
from sources.utility import pretty_print, animate_thinking

class Provider:
    def __init__(self, server_address="127.0.0.1:11434"):
        self.provider_name = "ollama"
        self.model = self._select_best_model()
        self.is_local = True
        self.server_ip = server_address
        self.server_address = server_address
        self.logger = Logger("provider.log")
        pretty_print(f"Using Ollama with model: {self.model}", color="success")

    def _select_best_model(self) -> str:
        """
        Automatically select the best available model from Ollama.
        Priority order: llama3.2, llama3.1, qwen2.5, mistral, codellama
        """
        preferred_models = [
            "llama3.2:latest",
            "llama3.1:latest",
            "qwen2.5:latest",
            "mistral:latest",
            "codellama:latest"
        ]

        try:
            host = f"http://{self.server_address}"
            client = OllamaClient(host=host)
            available_models = client.list()
            available_model_names = [model['name'] for model in available_models['models']]

            # Find the first preferred model that's available
            for model in preferred_models:
                if model in available_model_names:
                    return model

            # If no preferred models are available, use the first available model
            if available_model_names:
                return available_model_names[0]

            # If no models are available, default to llama3.2 (will be downloaded)
            return "llama3.2:latest"

        except Exception as e:
            pretty_print(f"Could not connect to Ollama, defaulting to llama3.2:latest", color="warning")
            return "llama3.2:latest"

    def get_model_name(self) -> str:
        return self.model

    def respond(self, history, verbose=True):
        """
        Use Ollama to generate text.
        """
        self.logger.info(f"Using Ollama with model: {self.model} at {self.server_ip}")
        try:
            thought = self.ollama_fn(history, verbose)
        except KeyboardInterrupt:
            self.logger.warning("User interrupted the operation with Ctrl+C")
            return "Operation interrupted by user. REQUEST_EXIT"
        except Exception as e:
            if "try again later" in str(e).lower():
                return f"Ollama server is overloaded. Please try again later."
            if "refused" in str(e):
                return f"Server {self.server_ip} seem offline. Unable to answer."
            raise Exception(f"Ollama failed: {str(e)}") from e
        return thought



    def ollama_fn(self, history, verbose=False):
        """
        Use local or remote Ollama server to generate text.
        """
        thought = ""
        host = "http://localhost:11434" if self.is_local else f"http://{self.server_address}"
        client = OllamaClient(host=host)

        try:
            stream = client.chat(
                model=self.model,
                messages=history,
                stream=True,
            )
            for chunk in stream:
                if verbose:
                    print(chunk["message"]["content"], end="", flush=True)
                thought += chunk["message"]["content"]
        except httpx.ConnectError as e:
            raise Exception(
                f"\nOllama connection failed at {host}. Check if the server is running."
            ) from e
        except Exception as e:
            if hasattr(e, 'status_code') and e.status_code == 404:
                animate_thinking(f"Downloading {self.model}...")
                client.pull(self.model)
                self.ollama_fn(history, verbose)
            if "refused" in str(e).lower():
                raise Exception(
                    f"Ollama connection refused at {host}. Is the server running?"
                ) from e
            raise e

        return thought




if __name__ == "__main__":
    provider = Provider()
    res = provider.respond([{"role": "user", "content": "Hello, how are you?"}])
    print("Response:", res)
