# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Preload the Hugging Face model during build
RUN python -c "\
from transformers import pipeline; \
pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')"

# Copy the rest of the application code
COPY . .

# Run tests to validate the application
RUN python -m unittest discover -s /app/tests -p "*.py"

# Expose the port
EXPOSE 8000

# Command to run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
