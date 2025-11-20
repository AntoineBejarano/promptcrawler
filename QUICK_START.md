# ⚡ Quick Start - 5 Minutos

## 🎯 Para Deploy en Railway

### Paso 1: Crear Servicios (2 min)

1. **Railway**: Ve a https://railway.app → "New Project" → Conecta tu repo
2. **Neon (Base de datos)**: Ve a https://neon.tech → Crea cuenta → Crea proyecto → Copia connection string
3. **Redis en Railway**: "+ New" → "Database" → "Add Redis"

✅ Railway automáticamente creará `REDIS_URL`
✅ Neon te dará `DATABASE_URL` (connection string)

### Paso 2: Configurar Variables (2 min)

En Railway, ve a tu servicio → "Variables" y añade:

```bash
# Base de datos (de Neon - pega tu connection string completa)
DATABASE_URL=postgresql://usuario:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require

# Redis (Railway lo genera automáticamente, pero verifica que esté)
REDIS_URL=redis://default:xxx@xxx.upstash.io:6379

# NextAuth
NEXTAUTH_SECRET=genera-uno-con-openssl-rand-base64-32
NEXTAUTH_URL=https://tu-app.railway.app

# API Keys
PERPLEXITY_API_KEY=pplx-tu-key

# URLs
NEXT_PUBLIC_API_URL=https://tu-app.railway.app
NEXT_PUBLIC_APP_URL=https://tu-app.railway.app
NODE_ENV=production
PYTHON_ENV=production
```

### Paso 3: Obtener API Key (1 min)

1. Ve a https://www.perplexity.ai/ → Crea cuenta → API Keys
2. Copia la key en `PERPLEXITY_API_KEY`

### Paso 4: Deploy

Railway desplegará automáticamente. ¡Listo! 🎉

---

## 🛠️ Para Desarrollo Local

```bash
# 1. Clonar y configurar
git clone <repo>
cd PromtCrawler
cp .env.example .env
# Editar .env con tus keys

# 2. Ejecutar
docker-compose up
```

Abre http://localhost:3000

---

## ❓ ¿Qué Base de Datos Usa?

- **PostgreSQL** → **Neon** (https://neon.tech) - Servicio externo, gratis
- **Redis** → Railway (añade como servicio Database → Redis)

**Neon** es PostgreSQL serverless, perfecto para este proyecto. Es gratis y muy fácil de usar.

---

¿Necesitas más ayuda? Ver:
- [GUIA_RAILWAY.md](./GUIA_RAILWAY.md) - Guía completa de Railway
- [SETUP_LOCAL.md](./SETUP_LOCAL.md) - Setup local detallado

