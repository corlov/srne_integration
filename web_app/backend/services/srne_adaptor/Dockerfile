# Use the official Python image from the Docker Hub
#FROM python:3.10-slim
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /monitor_app

# Copy the current directory contents into the container at /monitor_app
COPY . .

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
    
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# Define a health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python3 health_check.py

# Command to run the application
CMD ["python3", "srne_adaptor.py"]
