FROM python:3.10-slim

#Set user and copy files
USER 0
# Copy source files
#COPY . .
COPY requirements.txt .
RUN chgrp -R 0 requirements.txt && chmod -R g+rwX requirements.txt
RUN chown -R 1001:0 requirements.txt

COPY /app ./app
RUN chgrp -R 0 ./app && chmod -R g+rwX ./app 
RUN chown -R 1001:0 ./app
USER 1001

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Expose Gradio default port
EXPOSE 7860

# Run the app
CMD ["python", "gradio_chat.py"]
