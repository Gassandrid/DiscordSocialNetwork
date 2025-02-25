#!/bin/bash

# Function to display help
show_help() {
	echo "Discord Friend Scraper"
	echo
	echo "Usage:"
	echo "  ./run.sh [options]"
	echo
	echo "Options:"
	echo "  -e, --email EMAIL      Discord email address"
	echo "  -p, --password PASS    Discord password"
	echo "  -h, --help             Show this help message"
	echo "  -d, --debug            Enable debug mode (prints browser output)"
	echo
	echo "You can also use environment variables DISCORD_EMAIL and DISCORD_PASSWORD"
	echo
}

# Default values
DEBUG=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
	key="$1"
	case $key in
	-e | --email)
		export DISCORD_EMAIL="$2"
		shift
		shift
		;;
	-p | --password)
		export DISCORD_PASSWORD="$2"
		shift
		shift
		;;
	-d | --debug)
		DEBUG=true
		shift
		;;
	-h | --help)
		show_help
		exit 0
		;;
	*)
		echo "Unknown option: $1"
		show_help
		exit 1
		;;
	esac
done

# Check if credentials are provided
if [ -z "$DISCORD_EMAIL" ] || [ -z "$DISCORD_PASSWORD" ]; then
	# Try to load from .env file if it exists
	if [ -f .env ]; then
		echo "Loading credentials from .env file"
		export $(grep -v '^#' .env | xargs)
	fi

	# Check again after potentially loading from .env
	if [ -z "$DISCORD_EMAIL" ] || [ -z "$DISCORD_PASSWORD" ]; then
		echo "Error: Discord email and password are required."
		echo "You can provide them using command line options or environment variables."
		show_help
		exit 1
	fi
fi

# Create data directory if it doesn't exist
mkdir -p data

# Build and run the Docker container
if [ "$DEBUG" = true ]; then
	echo "Running in debug mode (output will be shown)"
	docker-compose up --build
else
	echo "Running in normal mode (building container...)"
	docker-compose up --build -d

	# Follow logs
	echo "Container is running. Showing logs (press Ctrl+C to stop viewing logs, container will continue running)"
	docker-compose logs -f
fi

echo "Results are saved in the data directory."
