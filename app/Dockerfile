# Python 3.11 base image for ECS Fargate
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables and port exposure
ENV PORT=8501
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]