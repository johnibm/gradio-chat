import gradio as gr
import json
import time
import os
from ol_prompt_query import *
from ollama import Client

# Load configuration


try:
    with open('./ol_config.json', 'r') as file:
        config = json.load(file)
        host = config.get('host', 'http://ollama:11434')
except Exception as e:
    print(f"Failed to load config: {e}")
    host = 'http://localhost:11434'

ollama_client = Client(host=host)

try:
    model_list = [m.model for item in ollama_client.list() for m in item[1]]
except Exception as e:
    raise RuntimeError("Ollama serve appears offline") from e

# Chat logic using OpenAI-style message format
def chat_with_model(user_input, model_name, temperature, max_tokens, use_context, history):
    print("=== chat_with_model called ===")
    print(f"user_input: {user_input}")
    print(f"model_name: {model_name}")

    if not user_input.strip() or model_name is None:
        history.append({"role": "assistant", "content": "Please provide input text and select a model before submitting."})
        return history, history

    # Append user message
    history.append({"role": "user", "content": user_input})

    if use_context:
       context = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in history)
       prompt = f"Question: {user_input}\nContext: {context}"
    else:
       prompt = user_input
