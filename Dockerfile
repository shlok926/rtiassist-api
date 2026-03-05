# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV HOST=0.0.0.0
ENV DEMO_MODE=true

# Copy and set startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run startup script (starts API + bot)
CMD ["/app/start.sh"]
