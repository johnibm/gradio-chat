FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY . .

# Expose Gradio default port
EXPOSE 7860

# Run the app
CMD ["python", "gradio_chat.py"]
