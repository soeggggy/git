FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY fly_requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r fly_requirements.txt

# Copy application code
COPY . .

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Command to run when container starts
CMD ["python", "fly_standalone.py"]