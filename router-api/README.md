# AgentRouter API

A FastAPI service for selecting appropriate agents based on user queries using the AgentRouter system.

## Features

- **Agent Selection**: Automatically selects the most appropriate agent based on user input
- **Language Detection**: Detects and translates multiple languages (English, French, Chinese)  
- **Complexity Estimation**: Estimates task complexity (HIGH/LOW)
- **Multi-Agent Support**: Supports Casual, Coder, File, and Browser agents
- **RESTful API**: Clean REST API with automatic documentation
- **Docker Support**: Containerized deployment with Docker

## API Endpoints

### Health Check
```
GET /health
```
Returns the service health status and number of loaded agents.

### Select Agent
```
POST /select-agent
```
Selects the appropriate agent based on input text.

**Request Body:**
```json
{
  "text": "Write a Python script to check network connectivity",
  "supported_languages": ["en", "fr", "zh"]
}
```

**Response:**
```json
{
  "selected_agent": "code_agent",
  "agent_name": "coder",
  "agent_role": "code",
  "complexity": "LOW",
  "confidence": 0.8,
  "language_detected": "en",
  "translated_text": null
}
```

### Estimate Complexity
```
POST /estimate-complexity
```
Estimates the complexity of a given text.

**Request Body:**
```json
{
  "text": "Create a machine learning model to predict stock prices"
}
```

**Response:**
```json
{
  "complexity": "HIGH",
  "confidence": 0.85
}
```

### List Agents
```
GET /agents
```
Returns information about all available agents.

### Root
```
GET /
```
Returns API information and available endpoints.

## Quick Start

### Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   python main.py
   ```

3. **Access the API:**
   - API: http://localhost:8080
   - Documentation: http://localhost:8080/docs
   - Health Check: http://localhost:8080/health

### Docker Deployment

1. **Build and Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually:**
   ```bash
   # From the project root directory
   docker build -f router-api/Dockerfile -t router-api .
   docker run -p 8080:8080 router-api
   ```

## Configuration

The API requires the following project structure:
- `sources/` - Core source code
- `llm_router/` - LLM router models
- `prompts/` - Agent prompt templates

Make sure these directories are available when running the API.

## Example Usage

### Using curl

```bash
# Health check
curl http://localhost:8080/health

# Select agent
curl -X POST "http://localhost:8080/select-agent" \
     -H "Content-Type: application/json" \
     -d '{"text": "Find a file called report.pdf on my drive"}'

# Estimate complexity
curl -X POST "http://localhost:8080/estimate-complexity" \
     -H "Content-Type: application/json" \
     -d '{"text": "Build a web scraper to collect news data"}'
```

### Using Python requests

```python
import requests

# Select agent
response = requests.post(
    "http://localhost:8080/select-agent",
    json={"text": "Debug this Python code"}
)
print(response.json())

# Estimate complexity
response = requests.post(
    "http://localhost:8080/estimate-complexity", 
    json={"text": "Create a neural network from scratch"}
)
print(response.json())
```

## CI/CD Pipeline

This project includes automated GitHub Actions workflows:

### 🚀 **Build and Push** (`build-router-api.yml`)
- **Trigger**: Push to `router` branch
- **Actions**: 
  - Builds multi-platform Docker image (linux/amd64, linux/arm64)
  - Pushes to GitHub Container Registry (`ghcr.io`)
  - Runs security vulnerability scanning with Trivy
  - Generates deployment summary

### 🧪 **Testing** (`test-router-api.yml`)  
- **Trigger**: Pull requests to `router` branch
- **Actions**:
  - Builds and tests Docker image
  - Runs API integration tests
  - Performs code linting and security checks
  - Validates dependencies for vulnerabilities

### Container Registry

Images are automatically published to:
```
ghcr.io/{owner}/agenticseek/router-api:router
```

### Production Deployment

Use the pre-built image from GitHub Container Registry:

```bash
# Pull the latest image
docker pull ghcr.io/yudaprama/agenticseek/router-api:router

# Run with production compose
docker-compose -f docker-compose.prod.yml up
```

## Dependencies

- FastAPI >= 0.115.0
- Uvicorn[standard] >= 0.30.0
- Transformers >= 4.46.0
- PyTorch >= 2.4.0
- Adaptive-classifier >= 0.0.10
- And other dependencies listed in requirements.txt

## Architecture

The API wraps the AgentRouter class and provides HTTP endpoints for:
- Agent selection based on text analysis
- Language detection and translation
- Task complexity estimation
- Agent information retrieval

## Error Handling

The API includes comprehensive error handling:
- 503: Service unavailable (router not initialized)
- 500: Internal server error (processing failures)
- 422: Validation error (invalid request data)

## Logging

The API logs all requests and responses to `router-api.log` for debugging and monitoring purposes. 