FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Hugging Face Spaces specifically look for port 7860
EXPOSE 7860

# Run the Gradio Dashboard as the main interface
CMD ["python", "app.py"]