# PromptCrawler

> **Tagline**: *"Convierte cualquier prompt en un dataset real de la web."*

PromptCrawler es una plataforma SaaS que convierte cualquier pregunta en un dataset real, buscado y scrapeado desde la web usando IA.

## Stack Técnico

- **Frontend**: Next.js 14 (React, TypeScript), Tailwind CSS, NextAuth, shadcn/ui
- **Backend**: FastAPI (Python), PostgreSQL, Redis + RQ, Crawl4AI, Perplexity API
- **Deployment**: Railway con Docker (frontend + backend en mismo container)

## Estructura del Proyecto

```
promptcrawler/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docker/           # Dockerfiles y configuraciones
├── docker-compose.yml
├── Dockerfile        # Dockerfile principal para Railway
└── README.md
```

## 🚀 Inicio Rápido

### Deploy en Railway (Producción)

1. **Crea proyecto en Railway** desde tu repo de GitHub
2. **Configura Neon** (PostgreSQL serverless): Ve a https://neon.tech → Crea proyecto → Copia connection string
3. **Añade Redis en Railway**: "+ New" → "Database" → "Add Redis"
4. **Configura variables de entorno** en Railway:
   - `DATABASE_URL` (connection string de Neon)
   - `REDIS_URL` (Railway lo genera automáticamente)
   - API keys y otros secrets
5. Railway desplegará automáticamente

📖 **Guías**:
- [QUICK_START.md](./QUICK_START.md) - Inicio rápido
- [GUIA_NEON.md](./GUIA_NEON.md) - Configurar Neon
- [GUIA_RAILWAY.md](./GUIA_RAILWAY.md) - Guía completa

### Desarrollo Local

Ver [SETUP_LOCAL.md](./SETUP_LOCAL.md) para instrucciones detalladas.

**Opción rápida con Docker:**

```bash
# 1. Copiar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 2. Ejecutar todo
docker-compose up
```

Accede a:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

## Variables de Entorno

Ver `.env.example` para la lista completa de variables requeridas.

## Deployment en Railway

El proyecto está configurado para deployarse en Railway usando Docker. Railway detectará automáticamente el `Dockerfile` y desplegará el proyecto.

## Licencia

MIT

