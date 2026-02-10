# Lottery Investment Calculator - Docker Setup

## 🐋 Docker Deployment Guide

### Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop)
- Docker Compose (included with Docker Desktop)

---

## 🚀 Quick Start

### 1. Build and Run Everything
```bash
docker-compose up -d
```

This will start:
- **Backend API** on http://localhost:5000
- **Frontend Web App** on http://localhost:3000

### 2. Check Status
```bash
docker-compose ps
```

### 3. View Logs
```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just frontend
docker-compose logs -f frontend
```

### 4. Stop Everything
```bash
docker-compose down
```

---

## 📦 Individual Services

### Backend Only
```bash
docker build -f Dockerfile.backend -t lottery-backend .
docker run -p 5000:5000 lottery-backend
```

### Frontend Only
```bash
docker build -f Dockerfile.frontend -t lottery-frontend .
docker run -p 3000:3000 lottery-frontend
```

### Email Scheduler (Optional)
```bash
docker-compose --profile email up -d
```

---

## 🔧 Configuration

### Update Next.js to use standalone output

Add to `frontend/next.config.ts`:
```typescript
const nextConfig = {
  output: 'standalone',
};
```

### Environment Variables

Create `.env` file:
```bash
# Backend
FLASK_ENV=production

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:5000

# Email (optional)
EMAIL_SENDER=mblanke@gmail.com
EMAIL_RECIPIENT=mblanke@gmail.com
EMAIL_PASSWORD=vyapvyjjfrqpqnax
```

Then update `docker-compose.yml` to use env_file:
```yaml
services:
  backend:
    env_file: .env
```

---

## 🏗️ Build Process

### First Time Setup
```bash
# Build all images
docker-compose build

# Or build individually
docker-compose build backend
docker-compose build frontend
docker-compose build email-scheduler
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

---

## 🌐 Network Configuration

All services communicate via the `lottery-network` bridge network.

### Internal URLs (container to container):
- Backend: `http://backend:5000`
- Frontend: `http://frontend:3000`

### External URLs (host to container):
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`

---

## 📊 Health Checks

The backend includes a health check endpoint:
```bash
curl http://localhost:5000/api/health
```

Check in Docker:
```bash
docker inspect lottery-backend | grep -A 10 Health
```

---

## 🔄 Production Deployment

### Docker Hub
```bash
# Tag images
docker tag lottery-backend yourusername/lottery-backend:latest
docker tag lottery-frontend yourusername/lottery-frontend:latest

# Push to Docker Hub
docker push yourusername/lottery-backend:latest
docker push yourusername/lottery-frontend:latest
```

### Deploy to Server
```bash
# Pull images on server
docker pull yourusername/lottery-backend:latest
docker pull yourusername/lottery-frontend:latest

# Run with compose
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check logs
docker logs lottery-backend

# Common issues:
# - Port 5000 already in use
# - Playwright installation failed
# - Missing dependencies
```

### Frontend can't connect to backend
```bash
# Check if backend is running
docker-compose ps

# Test backend directly
curl http://localhost:5000/api/health

# Check frontend environment
docker exec lottery-frontend env | grep API_URL
```

### Playwright browser issues
```bash
# Rebuild with no cache
docker-compose build --no-cache backend

# Check Playwright installation
docker exec lottery-backend playwright --version
```

### Container keeps restarting
```bash
# View logs
docker logs lottery-backend --tail 100

# Check health status
docker inspect lottery-backend | grep -A 5 Health
```

---

## 📝 Useful Commands

### Access Container Shell
```bash
# Backend
docker exec -it lottery-backend /bin/bash

# Frontend
docker exec -it lottery-frontend /bin/sh
```

### Remove Everything
```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Prune Unused Resources
```bash
docker system prune -a
```

### View Resource Usage
```bash
docker stats
```

---

## 🚢 Alternative: Docker without Compose

### Create Network
```bash
docker network create lottery-network
```

### Run Backend
```bash
docker run -d \
  --name lottery-backend \
  --network lottery-network \
  -p 5000:5000 \
  lottery-backend
```

### Run Frontend
```bash
docker run -d \
  --name lottery-frontend \
  --network lottery-network \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:5000 \
  lottery-frontend
```

---

## 🎯 Email Scheduler with Docker

To include the email scheduler:

1. **Start with email service:**
```bash
docker-compose --profile email up -d
```

2. **Or add to default profile** (edit docker-compose.yml):
Remove `profiles: - email` from email-scheduler service

3. **Check email logs:**
```bash
docker logs lottery-email -f
```

---

## 🔐 Security Notes

⚠️ **Important:**
- Never commit `.env` files with real credentials
- Use Docker secrets in production
- Set proper firewall rules
- Use HTTPS in production
- Regularly update base images

---

## 📈 Scaling

### Run multiple backend instances
```bash
docker-compose up -d --scale backend=3
```

### Add load balancer (nginx)
See `docker-compose.prod.yml` for nginx configuration

---

## 🆘 Support

If containers won't start:
1. Check Docker Desktop is running
2. Ensure ports 3000 and 5000 are available
3. Check logs: `docker-compose logs`
4. Rebuild: `docker-compose up -d --build`
5. Reset: `docker-compose down && docker-compose up -d`

---

## 📦 Image Sizes (Approximate)

- Backend: ~1.5 GB (includes Chromium browser)
- Frontend: ~200 MB
- Email Scheduler: ~1.5 GB (includes Chromium browser)

To reduce size, consider multi-stage builds or Alpine Linux variants.
