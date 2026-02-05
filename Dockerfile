# Use a lightweight Python version
FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure output is sent directly to logs
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 (Koyeb's default)
EXPOSE 8000

# Command to start the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
