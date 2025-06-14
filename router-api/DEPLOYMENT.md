# Router API Deployment Guide

This guide covers different deployment scenarios for the AgentRouter API.

## 🚀 Automated Deployment via GitHub Actions

### Prerequisites
- Push access to the `router` branch
- GitHub Container Registry access (automatic with GitHub account)

### Workflow
1. **Push to router branch** → Triggers automatic build and push
2. **Pull Request** → Runs tests and security checks
3. **Image available** at `ghcr.io/fosowl/agenticseek/router-api:router`

## 🐳 Container Deployment Options

### Option 1: Production Compose (Recommended)

```bash
# Download the production compose file
curl -O https://raw.githubusercontent.com/Fosowl/agenticSeek/router/router-api/docker-compose.prod.yml

# Create logs directory
mkdir -p logs

# Start the service
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Option 2: Direct Docker Run

```bash
# Pull the latest image
docker pull ghcr.io/fosowl/agenticseek/router-api:router

# Run the container
docker run -d \
  --name router-api \
  -p 8080:8080 \
  -v $(pwd)/logs:/app/.logs \
  --restart unless-stopped \
  ghcr.io/fosowl/agenticseek/router-api:router

# Check health
curl http://localhost:8080/health
```

### Option 3: Kubernetes Deployment

```yaml
# router-api-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: router-api
  labels:
    app: router-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: router-api
  template:
    metadata:
      labels:
        app: router-api
    spec:
      containers:
      - name: router-api
        image: ghcr.io/fosowl/agenticseek/router-api:router
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: router-api-service
spec:
  selector:
    app: router-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

```bash
# Deploy to Kubernetes
kubectl apply -f router-api-deployment.yml

# Check status
kubectl get pods -l app=router-api
kubectl get services router-api-service
```

## 🔧 Environment Configuration

### Required Environment Variables
```bash
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Optional Configuration
```bash
# Logging level
LOG_LEVEL=INFO

# Custom model paths (if using custom models)
LLM_ROUTER_PATH=/app/llm_router
PROMPTS_PATH=/app/prompts
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_loaded": 4
}
```

### Docker Health Check
The container includes built-in health checks:
```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Monitoring Setup with Prometheus

```yaml
# Add to docker-compose.prod.yml
version: '3.8'
services:
  router-api:
    # ... existing config
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=8080"
      - "prometheus.path=/metrics"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

## 🔐 Security Considerations

### Container Security
- Runs as non-root user
- Minimal base image (Python slim)
- Regular security scanning via Trivy
- No sensitive data in image layers

### Network Security
```bash
# Use custom network
docker network create router-network

# Run with custom network
docker run -d \
  --name router-api \
  --network router-network \
  -p 8080:8080 \
  ghcr.io/fosowl/agenticseek/router-api:router
```

### Access Control
- Use reverse proxy (nginx, traefik) for production
- Implement API key authentication if needed
- Enable HTTPS/TLS termination

## 🚨 Troubleshooting

### Common Issues

#### 1. Container fails to start
```bash
# Check logs
docker logs router-api

# Check resource usage
docker stats router-api
```

#### 2. Health check fails
```bash
# Test health endpoint directly
curl -v http://localhost:8080/health

# Check container network
docker network ls
docker inspect router-api
```

#### 3. Model loading errors
```bash
# Verify model files exist
docker exec router-api ls -la /app/llm_router/

# Check Python path
docker exec router-api python -c "import sys; print(sys.path)"
```

### Performance Issues

#### Memory Usage
```bash
# Monitor memory usage
docker stats --no-stream router-api

# Adjust memory limits in compose
services:
  router-api:
    deploy:
      resources:
        limits:
          memory: 4G  # Increase if needed
```

#### CPU Usage
```bash
# Monitor CPU usage
top -p $(docker inspect -f '{{.State.Pid}}' router-api)

# Scale horizontally
docker-compose up --scale router-api=3
```

## 🔄 Updates and Rollbacks

### Updating to Latest
```bash
# Pull latest image
docker pull ghcr.io/fosowl/agenticseek/router-api:router

# Restart with new image
docker-compose -f docker-compose.prod.yml up -d
```

### Rollback Strategy
```bash
# Tag specific versions for rollback
docker tag ghcr.io/fosowl/agenticseek/router-api:router \
           ghcr.io/fosowl/agenticseek/router-api:backup-$(date +%Y%m%d)

# Rollback to previous version
docker-compose -f docker-compose.prod.yml down
# Update image tag in compose file
docker-compose -f docker-compose.prod.yml up -d
```

## 📈 Scaling Considerations

### Horizontal Scaling
```bash
# Docker Compose scaling
docker-compose -f docker-compose.prod.yml up -d --scale router-api=3

# Load balancer (nginx example)
upstream router_api {
    server localhost:8080;
    server localhost:8081;
    server localhost:8082;
}
```

### Resource Requirements
- **Minimum**: 1GB RAM, 0.5 CPU
- **Recommended**: 2GB RAM, 1 CPU
- **High Load**: 4GB RAM, 2 CPU + horizontal scaling

## 📞 Support

For deployment issues:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review GitHub Actions logs
3. Create an issue with deployment details 