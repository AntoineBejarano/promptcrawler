# 🛠️ Setup Local - Desarrollo

Guía para ejecutar PromptCrawler en tu máquina local.

## 📋 Prerrequisitos

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (recomendado)
- PostgreSQL (si no usas Docker)
- Redis (si no usas Docker)

## 🚀 Opción 1: Docker Compose (Recomendado)

### 1. Clonar y configurar

```bash
# Clonar el repo
git clone <tu-repo>
cd PromtCrawler

# Copiar variables de entorno
cp .env.example .env

# Editar .env con tus valores
# Mínimo necesario:
# - PERPLEXITY_API_KEY
# - NEXTAUTH_SECRET (genera uno: openssl rand -base64 32)
```

### 2. Ejecutar con Docker Compose

```bash
docker-compose up
```

Esto iniciará:
- PostgreSQL en puerto 5432
- Redis en puerto 6379
- Backend en puerto 8000
- Frontend en puerto 3000
- Worker RQ

### 3. Acceder

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🚀 Opción 2: Desarrollo Manual

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/promptcrawler
# REDIS_URL=redis://localhost:6379/0
# PERPLEXITY_API_KEY=tu-key
# etc.

# Ejecutar
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXTAUTH_URL=http://localhost:3000
# NEXTAUTH_SECRET=tu-secret

# Ejecutar
npm run dev
```

### Worker (en otra terminal)

```bash
cd backend
source venv/bin/activate
python run_worker.py
```

### Base de Datos

**Opción 1: Usar Neon (Recomendado - igual que producción)**
1. Ve a https://neon.tech y crea un proyecto
2. Copia la connection string
3. Úsala en tu `.env` como `DATABASE_URL`
4. Las tablas se crean automáticamente al iniciar

**Opción 2: PostgreSQL Local**

```bash
# Crear base de datos
createdb promptcrawler

# O con PostgreSQL directamente
psql -U postgres
CREATE DATABASE promptcrawler;

# Las tablas se crean automáticamente al iniciar la app
# O puedes usar Alembic:
cd backend
alembic upgrade head
```

## 🔑 Obtener API Keys

### Perplexity
1. Ve a https://www.perplexity.ai/
2. Crea cuenta
3. Dashboard → API Keys
4. Genera una key

### OpenAI (Opcional)
1. Ve a https://platform.openai.com/
2. Crea cuenta
3. API Keys → Create new secret key

## ✅ Verificar que Funciona

1. Abre http://localhost:3000
2. Regístrate en /auth/register
3. Inicia sesión
4. Crea un job desde el dashboard
5. Verifica que el worker procese el job

## 🐛 Problemas Comunes

### Error de conexión a PostgreSQL
```bash
# Verifica que PostgreSQL esté corriendo
psql -U postgres -c "SELECT 1"

# O con Docker
docker ps | grep postgres
```

### Error de conexión a Redis
```bash
# Verifica que Redis esté corriendo
redis-cli ping

# Debe responder: PONG
```

### Puerto ya en uso
```bash
# Cambia los puertos en docker-compose.yml o en las variables de entorno
```

### Dependencias faltantes
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

