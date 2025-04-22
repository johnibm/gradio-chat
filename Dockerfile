FROM python:3.10-slim

#Set user and copy files
USER 0
# Copy source files
#COPY . .
COPY /app .
RUN chgrp -R 0 . && chmod -R g+rwX ./app 
RUN chown -R 1001:0 ./
USER 1001


# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose Gradio default port
EXPOSE 7860

# Run the app
CMD ["python", "gradio_chat.py"]
