# Dockerfile
# Use official Python image from Docker Hub
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the required files
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if you plan to set up an API)
EXPOSE 5000

# Run the Python script (entry point)
CMD ["python", "src/main.py"]
