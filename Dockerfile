# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install bash for start.sh and create a non-root user
RUN apt-get update && apt-get install -y bash && \
    useradd -m appuser

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 8085 for Flask app
EXPOSE 8085

# Use bash shell for start.sh
SHELL ["/bin/bash", "-c"]

# Use entrypoint to run start.sh
ENTRYPOINT ["./start.sh"]
