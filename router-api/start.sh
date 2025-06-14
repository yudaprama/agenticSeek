#!/bin/bash

# AgentRouter API Startup Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Starting AgentRouter API..."

# Check if required directories exist
REQUIRED_DIRS=("../sources" "../llm_router" "../prompts")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        print_error "Required directory $dir not found!"
        exit 1
    fi
done

# Build and start the services
print_status "Building Docker image..."
docker-compose build

print_status "Starting services..."
docker-compose up -d

# Wait for service to be healthy
print_status "Waiting for service to be ready..."
sleep 10

# Check if service is running
if curl -f http://localhost:8080/health &> /dev/null; then
    print_status "AgentRouter API is running successfully!"
    print_status "API URL: http://localhost:8080"
    print_status "API Documentation: http://localhost:8080/docs"
    print_status "Health Check: http://localhost:8080/health"
else
    print_warning "Service might still be starting up. Check logs with: docker-compose logs"
fi

print_status "To view logs: docker-compose logs -f"
print_status "To stop services: docker-compose down" 