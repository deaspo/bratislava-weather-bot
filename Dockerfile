# Bratislava Weather Bot - Dockerfile for Caprover deployment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cron \
        tzdata \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to Europe/Bratislava
ENV TZ=Europe/Bratislava
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Make scripts executable
RUN chmod +x main.py deploy.sh setup_cron.sh status.sh healthcheck.py

# Create cron job file
RUN echo "0 * * * * cd /app && python main.py --mode current >> logs/cron.log 2>&1" > /etc/cron.d/weather-bot

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/weather-bot

# Apply cron job
RUN crontab /etc/cron.d/weather-bot

# Create entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose port for health checks
EXPOSE 8080

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Set the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command
CMD ["python", "main.py", "--mode", "schedule"]
