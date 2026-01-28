# HealthPulse - Oracle Linux Deployment Setup Summary

## ✅ What Has Been Configured

### 1. **Traefik Reverse Proxy** (`docker-compose.traefik.yml`)
- Automatic SSL/TLS certificates via Let's Encrypt
- HTTP to HTTPS redirect
- Multi-environment support (prod/dev)
- Docker-based configuration (no manual nginx setup needed)

### 2. **CI/CD Pipeline** (`.github/workflows/cicd.yml`)
- Triggers on push to `main` and `develop` branches
- Runs backend tests with pytest
- Builds multi-architecture Docker images (amd64 + arm64)
- Pushes to GitHub Container Registry
- Deploys to Oracle Linux server via SSH
- Branch-based domain routing:
  - `main` → Production domain
  - `develop` → Development domain

### 3. **Deployment Scripts**
- `deploy.sh` - Manual deployment script (if needed)
- Automated deployment via GitHub Actions

### 4. **Documentation**
- `DEPLOYMENT.md` - Complete deployment guide
- `QUICK_START.md` - 15-minute quick start
- `SETUP_SUMMARY.md` - This file

---

## 📝 GitHub Secrets Required

You mentioned you've already added these secrets. Verify they're all set:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `SERVER_IP` | Oracle server IP address | `123.45.67.89` |
| `SSH_USER` | SSH username (usually `opc`) | `opc` |
| `SSH_PRIVATE_KEY` | SSH private key for authentication | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DOMAIN_PROD` | Production domain | `healthpulse.duckdns.org` |
| `DOMAIN_DEV` | Development domain | `dev.healthpulse.duckdns.org` |
| `ACME_EMAIL` | Email for Let's Encrypt SSL | `your@email.com` |

---

## 🚀 Next Steps

### Step 1: Prepare Oracle Server (One-Time Setup)

SSH into your Oracle server and run:

```bash
# Install Docker
sudo dnf update -y
sudo dnf install -y dnf-utils
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker opc

# Configure firewall
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Create deployment directory
mkdir -p /home/opc/healthpulse

# Log out and back in for group changes
exit
```

### Step 2: Configure Domains

Point your domains to your Oracle server IP:
- `DOMAIN_PROD` → Oracle server IP
- `DOMAIN_DEV` → Oracle server IP

**Recommended:** Use DuckDNS (https://www.duckdns.org/) for free subdomains.

### Step 3: Set Up SSH Key

On your local machine:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -f ~/.ssh/healthpulse_deploy

# Copy to Oracle server
ssh-copy-id -i ~/.ssh/healthpulse_deploy.pub opc@<your-server-ip>

# Display private key (add to GitHub Secret: SSH_PRIVATE_KEY)
cat ~/.ssh/healthpulse_deploy
```

### Step 4: Deploy!

```bash
# Deploy to development
git checkout develop
git add .
git commit -m "Initial deployment setup"
git push origin develop

# Deploy to production
git checkout main
git merge develop
git push origin main
```

### Step 5: Verify

After 3-5 minutes, visit:
- Development: `https://<DOMAIN_DEV>`
- Production: `https://<DOMAIN_PROD>`

---

## 🔍 Monitoring Deployment

### Watch GitHub Actions
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Watch the workflow progress

### Check Server Status

```bash
ssh opc@<your-server-ip>
cd /home/opc/healthpulse
docker compose -f docker-compose.traefik.yml ps
```

Expected output:
```
NAME                          STATUS
traefik                       Up
healthpulse-backend-prod      Up (healthy)
healthpulse-frontend-prod     Up
```

### View Logs

```bash
# All services
docker compose -f docker-compose.traefik.yml logs -f

# Specific service
docker logs traefik
docker logs healthpulse-backend-prod
```

---

## 🐛 Troubleshooting

### Issue: SSH Connection Failed in GitHub Actions

**Check:**
- SSH_PRIVATE_KEY secret is complete (including BEGIN/END lines)
- SSH_USER is correct (usually `opc` for Oracle Linux)
- SERVER_IP is accessible from internet

### Issue: Domain Not Accessible

**Check:**
- DNS propagation (use `nslookup <your-domain>`)
- Firewall ports 80/443 are open
- Containers are running (`docker ps`)

### Issue: SSL Certificate Error

**Wait 2-3 minutes** for Let's Encrypt to issue certificates. Check Traefik logs:
```bash
docker logs traefik | grep -i acme
```

---

## 📚 File Structure

```
.
├── .github/workflows/
│   └── cicd.yml                    # CI/CD pipeline
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   ├── Dockerfile
│   └── nginx/
│       └── default.conf
├── docker-compose.yml              # Original local development
├── docker-compose.traefik.yml      # Production with Traefik
├── deploy.sh                       # Manual deployment script
├── .env.production.example         # Example env file
├── .env.development.example        # Example env file
├── DEPLOYMENT.md                   # Full deployment guide
├── QUICK_START.md                  # Quick start guide
└── SETUP_SUMMARY.md               # This file
```

---

## 🎯 What Happens on Push

1. **Code pushed to `develop` or `main`**
2. **GitHub Actions triggers:**
   - Runs pytest tests
   - Builds Docker images
   - Pushes to GHCR
   - SSHs to Oracle server
   - Copies docker-compose.traefik.yml
   - Creates .env file with correct domain
   - Pulls latest images
   - Restarts containers
3. **Traefik automatically:**
   - Routes traffic based on domain
   - Generates SSL certificates
   - Proxies to correct containers

---

## 📞 Support

For detailed instructions, see:
- **Quick Setup:** [QUICK_START.md](./QUICK_START.md)
- **Full Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)

