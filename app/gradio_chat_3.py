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

# Chat logic 
def chat_with_model(user_input, model_name, temperature, max_tokens, use_context, history):
    print("=== chat_with_model called ===")
    print(f"user_input: {user_input}")
    print(f"model_name: {model_name}")

    if not user_input.strip() or model_name is None:
        history.append({"role": "assistant", "content": "Please provide input text and select a model before submitting."})
        return history, history

    history.append({"role": "user", "content": user_input})

    if use_context:
        context = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in history)
        prompt = f"Question: {user_input}\nContext: {context}"
    else:
        prompt = user_input

    assistant_content = ""
    # Yield a "thinking" message
    yield history + [{"role": "assistant", "content": f"🤖 Analysing: {user_input}..."}], history

    # Generate response using query3
    for chunk in query3(model_name, prompt, temperature, max_tokens):
        assistant_content += chunk
        yield history + [{"role": "assistant", "content": assistant_content}], history

    history.append({"role": "assistant", "content": assistant_content})
    yield history, history
# Utility: Clear conversation
def clear_chat():
    return [], []

# Utility: Save conversation to JSON
def save_chat(history):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fn = f"chat-{timestr}.json"
    conversation = {
        "conversation": {
            "timestamp": timestr,
            "content": [{"role": role, "content": msg} for role, msg in history]
        }
    }
    with open(fn, 'w') as fd:
        json.dump(conversation, fd)
    return f"Saved to {os.getcwd()}/{fn}"

# UI definition
with gr.Blocks(title="ε.chat v2.0") as demo:
    gr.Markdown("## 💬 ε.chat v2.0")

    with gr.Row():
        model_dropdown = gr.Dropdown(choices=model_list, label="Model Selection")
        temp_slider = gr.Slider(0.0, 1.0, value=0.7, label="Temperature")
        max_tokens_input = gr.Number(value=256, label="Max Tokens", precision=0)
        use_context_toggle = gr.Checkbox(label="Use Context", value=True)

    #chatbot = gr.Chatbot(label="Conversation")
    chatbot = gr.Chatbot(label="Conversation", type="messages")

    user_input = gr.Textbox(placeholder="Type or paste your message here...", label="Your message")

    with gr.Row():
        clear_btn = gr.Button("🗑️ Clear Conversation")
        save_btn = gr.Button("💽 Save Conversation")

    state = gr.State([])

    user_input.submit(
        chat_with_model,
        inputs=[user_input, model_dropdown, temp_slider, max_tokens_input, use_context_toggle, state],
        outputs=[chatbot, state]
    )

    clear_btn.click(fn=clear_chat, outputs=[chatbot, state])
    save_btn.click(fn=save_chat, inputs=state, outputs=None)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
