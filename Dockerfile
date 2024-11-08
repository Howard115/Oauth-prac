# Use Ubuntu 24.04 as base image
FROM ubuntu:24.04

# Set working directory
WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# Create and activate virtual environment 
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"


# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/
COPY run_app.py .

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python3", "run_app.py"]
