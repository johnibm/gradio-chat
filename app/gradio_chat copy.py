import gradio as gr
import json
import time
import os
from ol_prompt_query import *
from ollama import Client

# Load configuration
with open('./ol_config.json', 'r') as file:
    config = json.load(file)

host = config['host']
ollama_client = Client(host=host)

try:
    model_list = [m.model for item in ollama_client.list() for m in item[1]]
except Exception as e:
    raise RuntimeError("Ollama serve appears offline") from e

# Session state equivalent
chat_history = []

def chat_with_model(user_input, model_name, temperature, max_tokens, use_context, history):
    if not user_input.strip() or model_name is None:
        return history + [("Error", "Please provide input text and select a model before submitting.")], history

    # Append user message
    history.append(("You", user_input))

    # Construct prompt
    if use_context:
        context = "\n".join(f"{role}: {msg}" for role, msg in history if role == "You" or role == model_name)
        prompt = f"Question: {user_input} Context: {context}"
    else:
        prompt = user_input

    assistant_content = ""
    yield history + [(model_name, f"🤖 Analysing: {user_input}...")], history

    for chunk in query3(model_name, prompt, temperature, max_tokens):
        assistant_content += chunk
        yield history + [(model_name, assistant_content)], history

    #history.append((model_name, assistant_content))
    history.append(("Assistant", assistant_content))
    yield history, history

def clear_chat():
    return [], []

def save_chat(history):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fn = f"chat-{timestr}.json"
    conversation = {"conversation": {"timestamp": timestr, "content": [{"role": role, "content": msg} for role, msg in history]}}
    with open(fn, 'w') as fd:
        json.dump(conversation, fd)
    return f"Saved to {os.getcwd()}/{fn}"

with gr.Blocks(title="ε.chat v2.0") as demo:
    gr.Markdown("## 💬 ε.chat v2.0")

    with gr.Row():
        model_dropdown = gr.Dropdown(choices=model_list, label="Model Selection")
        temp_slider = gr.Slider(0.0, 1.0, value=0.7, label="Temperature")
        max_tokens_input = gr.Number(value=256, label="Max Tokens", precision=0)
        use_context_toggle = gr.Checkbox(label="Use Context", value=True)

    chatbot = gr.Chatbot(label="Conversation")
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
