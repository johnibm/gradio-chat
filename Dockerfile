FROM python:3.10-slim

#Set user and copy files
USER 0

#Install curl
RUN apt-get update && apt-get install -y curl

# Copy source files
#COPY . .
COPY /app /app
RUN chgrp -R 0 /app && chmod -R g+rwX /app 
RUN chown -R 1001:0 /app
# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install -U "pip>=23.3.1" && \
    pip install --no-cache-dir -r requirements.txt

USER 1001

# Expose Gradio default port
EXPOSE 7860

# Run the app
CMD ["python", "gradio_chat.py"]
