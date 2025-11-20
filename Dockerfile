# Multi-stage Dockerfile para Railway
# Frontend + Backend en el mismo container

# ============================================
# Stage 1: Build Frontend
# ============================================
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copiar archivos de dependencias
COPY frontend/package*.json ./

# Instalar dependencias
RUN npm ci --only=production=false

# Copiar código del frontend
COPY frontend/ .

# Build del frontend
RUN npm run build

# ============================================
# Stage 2: Build Backend
# ============================================
FROM python:3.11-slim AS backend-builder

WORKDIR /app/backend

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 3: Production Image
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Instalar Node.js para servir el frontend
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar Python dependencies del builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copiar backend
COPY backend/ ./backend/

# Copiar frontend build
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY --from=frontend-builder /app/frontend/package*.json ./frontend/
COPY --from=frontend-builder /app/frontend/next.config.js ./frontend/
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules

# Exponer puertos
EXPOSE 8000 3000

# Script de inicio
COPY docker/railway-start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

