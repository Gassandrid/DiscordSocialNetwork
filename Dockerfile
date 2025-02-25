# Use Python 3.12 as base image
FROM python:3.12-slim

# Install system dependencies including Chrome
RUN apt-get update && apt-get install -y \
  wget \
  gnupg2 \
  curl \
  unzip \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Chrome WebDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
  && wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
  && rm /tmp/chromedriver.zip \
  && chmod +x /usr/local/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Set environment variables for headless Chrome
ENV DISPLAY=:99
ENV CHROME_OPTIONS="--headless --no-sandbox --disable-dev-shm-usage"

# Command to run the script
CMD ["python", "src/discordsocialnetwork/scrape.py"]

