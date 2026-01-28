#!/bin/bash
set -e

# Deployment script for HealthPulse
# Usage: ./deploy.sh [production|development]

ENVIRONMENT=${1:-production}
DEPLOY_DIR="/home/${SSH_USER:-opc}/healthpulse"

echo "🚀 Deploying HealthPulse to ${ENVIRONMENT} environment..."

# Create deployment directory if it doesn't exist
mkdir -p "${DEPLOY_DIR}"
cd "${DEPLOY_DIR}"

# Create .env file based on environment
if [ "${ENVIRONMENT}" = "production" ]; then
    cat > .env <<EOF
REGISTRY=${REGISTRY}
IMAGE_PREFIX=${IMAGE_PREFIX}
TAG=${TAG}
ENVIRONMENT=prod
DOMAIN=${DOMAIN_PROD}
ACME_EMAIL=${ACME_EMAIL}
EOF
else
    cat > .env <<EOF
REGISTRY=${REGISTRY}
IMAGE_PREFIX=${IMAGE_PREFIX}
TAG=${TAG}
ENVIRONMENT=dev
DOMAIN=${DOMAIN_DEV}
ACME_EMAIL=${ACME_EMAIL}
EOF
fi

echo "✅ Environment file created"

# Pull latest images
echo "📥 Pulling Docker images..."
docker compose -f docker-compose.traefik.yml pull

# Start/restart services
echo "🔄 Starting services..."
docker compose -f docker-compose.traefik.yml up -d

# Show running containers
echo "📊 Running containers:"
docker compose -f docker-compose.traefik.yml ps

# Cleanup old images
echo "🧹 Cleaning up old images..."
docker image prune -f

echo "✅ Deployment complete!"
echo "🌐 Application should be available at: https://${DOMAIN}"

