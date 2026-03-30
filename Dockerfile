# Use lightweight Python 3.10 image which is highly compatible with CrewAI
FROM python:3.10.14-slim

# Set working directory
WORKDIR /app

# Install system dependencies (sometimes needed for building crewai tools)
RUN apt-get update && \
    apt-get install -y gcc g++ build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the API port
EXPOSE 10000

# Start the FastAPI server using Uvicorn (Render uses the PORT environment variable)
CMD ["sh", "-c", "uvicorn push_to_mongo:app --host 0.0.0.0 --port ${PORT:-10000}"]