FROM python:3.9-slim

# Install Chromium and related dependencies
RUN apt-get update && apt-get install -y \
  chromium \
  chromium-driver \
  wget \
  unzip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY discord_scraper.py .

# Create a volume for output data
VOLUME /app/data

# Set environment variables for Chromium
ENV CHROME_OPTIONS="--headless --no-sandbox --disable-dev-shm-usage"
ENV CHROMIUM_PATH="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Command to run the script
ENTRYPOINT ["python", "discord_scraper.py"]
