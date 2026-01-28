# HealthPulse - Quick Start Guide

## ⚡ TL;DR - Get Running in 15 Minutes

### 1. Server Setup (5 minutes)

```bash
# SSH into Oracle server
ssh opc@<your-server-ip>

# Install Docker
sudo dnf update -y
sudo dnf install -y dnf-utils
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Configure firewall
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Create directory
mkdir -p /home/opc/healthpulse

# Log out and back in
exit
```

### 2. Domain Setup (3 minutes)

**Using DuckDNS (easiest):**
1. Go to https://www.duckdns.org/
2. Create two subdomains pointing to your Oracle server IP:
   - `yourapp.duckdns.org`
   - `yourapp-dev.duckdns.org`

### 3. SSH Key Setup (2 minutes)

```bash
# On your local machine
ssh-keygen -t ed25519 -f ~/.ssh/healthpulse_deploy
ssh-copy-id -i ~/.ssh/healthpulse_deploy.pub opc@<your-server-ip>
cat ~/.ssh/healthpulse_deploy  # Copy this for GitHub
```

### 4. GitHub Secrets (3 minutes)

Add these in GitHub → Settings → Secrets and variables → Actions:

```
SERVER_IP=<your-oracle-ip>
SSH_USER=opc
SSH_PRIVATE_KEY=<paste-private-key-here>
DOMAIN_PROD=yourapp.duckdns.org
DOMAIN_DEV=yourapp-dev.duckdns.org
ACME_EMAIL=your@email.com
```

### 5. Deploy (2 minutes)

```bash
git push origin develop  # Deploys to dev domain
git push origin main     # Deploys to prod domain
```

**Done!** Visit your domains in 2-3 minutes after push.

---

## 🔍 Verify Everything Works

```bash
# Check containers are running
ssh opc@<your-server-ip>
docker ps

# Should see: traefik, healthpulse-backend-*, healthpulse-frontend-*
```

Visit your domains:
- `https://yourapp-dev.duckdns.org` (develop branch)
- `https://yourapp.duckdns.org` (main branch)

---

## 🐛 Common Issues

### Issue: "Connection refused" when accessing domain

**Solution:**
```bash
# Check if containers are running
docker ps

# Check firewall
sudo firewall-cmd --list-all

# Restart services
cd /home/opc/healthpulse
docker compose -f docker-compose.traefik.yml restart
```

### Issue: "SSL certificate error"

**Solution:** Wait 2-3 minutes for Let's Encrypt to issue certificates. Check Traefik logs:
```bash
docker logs traefik
```

### Issue: "502 Bad Gateway"

**Solution:** Backend might not be healthy yet. Check:
```bash
docker compose -f docker-compose.traefik.yml ps
docker logs healthpulse-backend-prod  # or -dev
```

---

## 📚 Full Documentation

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete details.

