# Pre-Deployment Checklist

Use this checklist to ensure everything is ready before deploying.

## ✅ Oracle Server Setup

- [ ] Oracle Linux 9 server is running
- [ ] You have SSH access to the server
- [ ] Server IP address is noted: `___________________`
- [ ] Docker is installed on the server
- [ ] Docker Compose plugin is installed
- [ ] Firewall ports 80 and 443 are open
- [ ] User is added to docker group
- [ ] Directory `/home/opc/healthpulse` exists

### Quick Verification Commands

```bash
# Test SSH access
ssh opc@<your-server-ip>

# Verify Docker
docker --version
docker compose version

# Check firewall
sudo firewall-cmd --list-all | grep -E "http|https"

# Verify directory
ls -la /home/opc/healthpulse
```

---

## ✅ Domain Configuration

- [ ] Production domain is registered: `___________________`
- [ ] Development domain is registered: `___________________`
- [ ] Both domains point to Oracle server IP
- [ ] DNS propagation is complete (wait 5-30 minutes)

### Verify DNS

```bash
# From your local machine
nslookup <your-prod-domain>
nslookup <your-dev-domain>

# Both should return your Oracle server IP
```

---

## ✅ GitHub Secrets

Go to: **GitHub Repository → Settings → Secrets and variables → Actions**

- [ ] `SERVER_IP` is set
- [ ] `SSH_USER` is set (usually `opc`)
- [ ] `SSH_PRIVATE_KEY` is set (complete key with BEGIN/END lines)
- [ ] `DOMAIN_PROD` is set
- [ ] `DOMAIN_DEV` is set
- [ ] `ACME_EMAIL` is set

### Verify Secrets

In GitHub, you should see 6 secrets listed (you can't view values, only names).

---

## ✅ SSH Key Setup

- [ ] SSH key pair generated
- [ ] Public key copied to Oracle server
- [ ] Private key added to GitHub Secrets
- [ ] Can SSH without password prompt

### Test SSH Connection

```bash
# Should connect without asking for password
ssh -i ~/.ssh/healthpulse_deploy opc@<your-server-ip>
```

---

## ✅ Code Repository

- [ ] All new files are committed
- [ ] `.gitignore` is updated
- [ ] `develop` branch exists
- [ ] `main` branch exists
- [ ] GitHub Actions is enabled

### Verify Files

```bash
git status
git branch -a
```

Expected new files:
- `docker-compose.traefik.yml`
- `.github/workflows/cicd.yml` (updated)
- `DEPLOYMENT.md`
- `QUICK_START.md`
- `SETUP_SUMMARY.md`
- `PRE_DEPLOYMENT_CHECKLIST.md`
- `.env.production.example`
- `.env.development.example`
- `deploy.sh`

---

## ✅ Final Pre-Flight Checks

- [ ] All tests pass locally: `pytest -q`
- [ ] Docker images build successfully locally
- [ ] No sensitive data in repository
- [ ] `.env` files are in `.gitignore`
- [ ] Documentation is up to date

### Run Local Tests

```bash
# Backend tests
cd backend
python -m pip install -r requirements.txt
cd ..
PYTHONPATH=. pytest -q

# Build Docker images locally (optional)
docker compose -f docker-compose.traefik.yml build
```

---

## 🚀 Ready to Deploy?

If all items above are checked, you're ready to deploy!

### Deploy to Development

```bash
git checkout develop
git add .
git commit -m "Setup Oracle Linux deployment with Traefik"
git push origin develop
```

### Monitor Deployment

1. Go to GitHub → Actions tab
2. Watch the workflow run
3. Wait 3-5 minutes for completion
4. Visit `https://<DOMAIN_DEV>`

### Deploy to Production

```bash
git checkout main
git merge develop
git push origin main
```

Visit `https://<DOMAIN_PROD>` after 3-5 minutes.

---

## 🐛 If Something Goes Wrong

### Check GitHub Actions Logs
- Go to Actions tab in GitHub
- Click on the failed workflow
- Review error messages

### Check Server Logs

```bash
ssh opc@<your-server-ip>
cd /home/opc/healthpulse
docker compose -f docker-compose.traefik.yml logs -f
```

### Common Issues

1. **SSH connection failed**: Check SSH_PRIVATE_KEY secret
2. **Domain not accessible**: Check DNS and firewall
3. **SSL errors**: Wait 2-3 minutes for Let's Encrypt
4. **502 Bad Gateway**: Backend not healthy, check logs

---

## 📞 Need Help?

Refer to:
- [QUICK_START.md](./QUICK_START.md) - Fast setup guide
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Detailed instructions
- [SETUP_SUMMARY.md](./SETUP_SUMMARY.md) - Overview

---

## ✨ Post-Deployment

After successful deployment:

- [ ] Production site is accessible via HTTPS
- [ ] Development site is accessible via HTTPS
- [ ] SSL certificates are valid (green padlock)
- [ ] Application functions correctly
- [ ] Both environments are independent

### Celebrate! 🎉

Your HealthPulse application is now deployed with:
- ✅ Automatic SSL/TLS
- ✅ Multi-environment support
- ✅ CI/CD pipeline
- ✅ Zero-downtime deployments
- ✅ Production-ready infrastructure

