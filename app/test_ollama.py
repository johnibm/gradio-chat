import json
import requests
import os

def test_ollama_api():
    ollama_host = os.getenv("OLLAMA_HOST", "localhost")  # fallback to localhost if not set
    url = f"http://{ollama_host}:11434/v1/completions"
    
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "zephyr:latest",  # Replace with the model you're using
        "prompt": "Hello, how are you?",  # Example prompt to test
        "temperature": 0.7,
        "max_tokens": 256,
        "stream": False  # Set stream=False for this test
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Success! Response: {response.json()}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error making request: {str(e)}")

if __name__ == "__main__":
    test_ollama_api()
