# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment
RUN python -m venv /env

# Set environment variable to use the virtual environment
ENV PATH="/env/bin:$PATH"

# Copy the application's requirements file and install dependencies
COPY requirements.txt .

# Install dependencies inside the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
