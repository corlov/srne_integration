# Use the official Python image from the Docker Hub
#FROM python:3.10-slim
FROM python:3.10-slim


# Copy the current directory contents into the container at /monitor_app
COPY . .

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
    
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# Command to run the application
CMD ["python3", "lamp_mode.py"]

