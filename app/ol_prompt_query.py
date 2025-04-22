import json
import requests
import os

ollama_host = os.getenv("OLLAMA_HOST", "localhost")  # fallback to localhost if not set
url = f"http://{ollama_host}:11434/v1/completions"

def query3(model_name, prompt, temperature, max_tokens):
    """
    This function sends the user's prompt to the Ollama model API and streams the response.
    Args:
        model_name (str): The name of the model to use.
        prompt (str): The user input prompt.
        temperature (float): The temperature for randomness in response generation.
        max_tokens (int): Maximum number of tokens in the response.
    
    Yields:
        str: Response chunks as they become available from the API.
    """

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "model": model_name,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False  # To stream the response.
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        # Check if the response is successful
        if response.status_code == 200:
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    chunk_data = json.loads(chunk)
                    if "text" in chunk_data:
                        yield chunk_data["text"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error in query3: {str(e)}")
        return

