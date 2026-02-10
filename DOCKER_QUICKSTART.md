# 🐋 Docker Setup Complete!

## What's Been Created

### Docker Files
- ✅ `Dockerfile.backend` - Flask API with Playwright
- ✅ `Dockerfile.frontend` - Next.js app optimized for production
- ✅ `Dockerfile.email` - Email scheduler service
- ✅ `docker-compose.yml` - Development setup
- ✅ `docker-compose.prod.yml` - Production setup with nginx
- ✅ `.dockerignore` - Optimized build context
- ✅ `requirements.txt` - Python dependencies

### Configuration
- ✅ Updated `next.config.ts` for standalone output
- ✅ Created startup scripts (Windows & Linux)
- ✅ Complete documentation in `DOCKER_README.md`

---

## 🚀 Quick Start

### Option 1: Windows Script (Easiest)
```bash
docker-start.bat
```

### Option 2: Docker Compose
```bash
docker-compose up -d
```

### Option 3: Manual Build
```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Check status
docker-compose ps
```

---

## 📦 What Gets Deployed

### Backend Container
- Python 3.13
- Flask API on port 5000
- Playwright with Chromium browser
- Lottery scrapers for all 4 lotteries
- Investment calculator
- Health check endpoint

### Frontend Container
- Node.js 20
- Next.js standalone build
- Optimized production bundle
- Connects to backend API

### Email Container (Optional)
- Runs daily at 7:00 AM
- Sends lottery jackpot emails
- Uses same scraping logic

---

## 🌐 Access Points

After running `docker-compose up -d`:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

---

## 📊 Container Management

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services
```bash
docker-compose restart
```

### Stop Everything
```bash
docker-compose down
```

### Rebuild After Changes
```bash
docker-compose up -d --build
```

---

## 🔧 Troubleshooting

### Port Already in Use
If ports 3000 or 5000 are busy:

**Option A**: Stop other services
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Option B**: Change ports in `docker-compose.yml`
```yaml
ports:
  - "8080:3000"  # Use port 8080 instead
```

### Backend Won't Start
```bash
# Check logs
docker logs lottery-backend

# Rebuild without cache
docker-compose build --no-cache backend
```

### Frontend Can't Connect
Update `docker-compose.yml` frontend environment:
```yaml
environment:
  - NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

## 🎯 Include Email Scheduler

To run the email scheduler:

```bash
docker-compose --profile email up -d
```

Or remove the `profiles` section from `docker-compose.yml` to always include it.

---

## 📈 Production Deployment

### Use Production Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Deploy to Server
```bash
# On your server
git clone <your-repo>
cd Lottery
docker-compose -f docker-compose.prod.yml up -d
```

### Push to Docker Hub
```bash
# Login
docker login

# Tag images
docker tag lottery-backend yourusername/lottery-backend:latest
docker tag lottery-frontend yourusername/lottery-frontend:latest

# Push
docker push yourusername/lottery-backend:latest
docker push yourusername/lottery-frontend:latest
```

---

## 🔒 Security for Production

1. **Use environment variables** - Don't hardcode credentials
2. **Enable HTTPS** - Use nginx with SSL certificates
3. **Update base images** regularly
4. **Scan for vulnerabilities**:
   ```bash
   docker scan lottery-backend
   ```
5. **Use Docker secrets** for sensitive data

---

## 💾 Data Persistence

Currently, containers are stateless. To add persistence:

Add volumes in `docker-compose.yml`:
```yaml
volumes:
  - ./data:/app/data
```

---

## 🎛️ Resource Limits

Current limits (production):
- Backend: 2GB RAM, 1 CPU
- Frontend: 512MB RAM, 0.5 CPU
- Email: 1GB RAM, 0.5 CPU

Adjust in `docker-compose.prod.yml` if needed.

---

## ✅ Benefits of Docker

1. ✅ **Consistent environment** - Works the same everywhere
2. ✅ **Easy deployment** - One command to start everything
3. ✅ **Isolation** - Each service in its own container
4. ✅ **Scalability** - Easy to scale services
5. ✅ **Version control** - Docker images are versioned
6. ✅ **Portability** - Deploy anywhere Docker runs

---

## 📝 Next Steps

1. ✅ Test locally: `docker-compose up -d`
2. ✅ Check logs: `docker-compose logs -f`
3. ✅ Access app: http://localhost:3000
4. ✅ Configure email scheduler if needed
5. ✅ Deploy to production server
6. ✅ Set up CI/CD pipeline (optional)

---

## 🆘 Need Help?

See detailed documentation in:
- `DOCKER_README.md` - Full Docker guide
- `EMAIL_SETUP.md` - Email configuration
- Docker logs: `docker-compose logs -f`

---

Enjoy your Dockerized Lottery Investment Calculator! 🎰🐋
