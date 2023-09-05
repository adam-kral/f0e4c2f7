# Use the official Python image from the Docker Hub
FROM python:3.11-slim-buster

# Disable output buffering
ENV PYTHONUNBUFFERED=1

# Make a directory for our application
WORKDIR /app

# Copy all files from our local machine project into the /app folder inside the container
COPY . .

# Use pip to install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run our Python application when the container starts
ENTRYPOINT ["python", "./src/flask_app.py"]
