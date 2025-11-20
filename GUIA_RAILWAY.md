# 🚀 Guía Completa: Deploy en Railway - Paso a Paso

## 📋 Resumen

Este proyecto usa:
- **PostgreSQL** como base de datos (NO se crea automáticamente)
- **Redis** para la cola de trabajos (NO se crea automáticamente)
- **FastAPI** (backend) en puerto 8000
- **Next.js** (frontend) en puerto 3000

## 🎯 Pasos para Deploy

### 1️⃣ Crear Proyecto en Railway

1. Ve a https://railway.app
2. Inicia sesión (puedes usar GitHub)
3. Click en **"New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Conecta tu repositorio de GitHub donde está este código
6. Railway detectará el `Dockerfile` automáticamente

### 2️⃣ Crear Base de Datos con Neon

**Usaremos Neon** (PostgreSQL serverless) en lugar de PostgreSQL de Railway:

1. Ve a https://neon.tech y crea una cuenta (gratis)
2. Crea un nuevo proyecto
3. Neon te dará una **Connection String** que se ve así:
   ```
   postgresql://usuario:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require
   ```
4. Copia esta connection string completa
5. En Railway, ve a tu servicio → **"Variables"** → Añade:
   ```
   DATABASE_URL=postgresql://usuario:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require
   ```
   (Pega tu connection string completa de Neon)

### 3️⃣ Crear Redis

1. En tu proyecto de Railway, click en **"+ New"** o **"Add Service"**
2. Selecciona **"Database"** → **"Add Redis"**
3. Railway creará un servicio Redis
4. **Automáticamente** generará la variable de entorno `REDIS_URL`
5. Esta variable se inyectará en tu aplicación automáticamente

### 4️⃣ Configurar Variables de Entorno

En tu servicio principal (el que tiene el Dockerfile), ve a **"Variables"** y añade:

#### Variables Requeridas:

```bash
# NextAuth (genera un secret aleatorio)
NEXTAUTH_SECRET=tu-secret-super-seguro-aqui-minimo-32-caracteres
NEXTAUTH_URL=https://tu-app.railway.app

# API Keys (obtén estas de los proveedores)
PERPLEXITY_API_KEY=pplx-tu-api-key-aqui
OPENAI_API_KEY=sk-tu-api-key-aqui  # Opcional

# URLs de la aplicación
NEXT_PUBLIC_API_URL=https://tu-app.railway.app
NEXT_PUBLIC_APP_URL=https://tu-app.railway.app
BACKEND_URL=http://localhost:8000

# Environment
NODE_ENV=production
PYTHON_ENV=production
```

#### ⚠️ IMPORTANTE sobre las URLs:

Cuando Railway despliegue tu app, te dará una URL como:
- `https://tu-app-production.up.railway.app`

**Usa esa URL** en:
- `NEXTAUTH_URL`
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_APP_URL`

### 5️⃣ Obtener API Keys

#### Perplexity API:
1. Ve a https://www.perplexity.ai/
2. Crea una cuenta
3. Ve a tu dashboard de API
4. Genera una API key
5. Cópiala en `PERPLEXITY_API_KEY`

#### OpenAI API (Opcional):
1. Ve a https://platform.openai.com/
2. Crea una cuenta
3. Ve a API Keys
4. Genera una nueva key
5. Cópiala en `OPENAI_API_KEY`

### 6️⃣ Generar NEXTAUTH_SECRET

Puedes generar un secret seguro con:

```bash
# En tu terminal local
openssl rand -base64 32
```

O usa cualquier generador de strings aleatorios (mínimo 32 caracteres).

### 7️⃣ Configurar Dominio (Opcional)

1. En Railway, ve a tu servicio
2. Click en **"Settings"** → **"Generate Domain"**
3. Railway te dará una URL pública
4. Actualiza las variables de entorno con esa URL

### 8️⃣ Inicializar Base de Datos

La aplicación creará las tablas automáticamente al iniciar (ver `backend/app/main.py` línea 12: `Base.metadata.create_all(bind=engine)`).

Si prefieres usar migraciones de Alembic:

1. En Railway, ve a tu servicio
2. Click en **"Deployments"** → **"..."** → **"Run Command"**
3. Ejecuta:
   ```bash
   cd backend && alembic upgrade head
   ```

### 9️⃣ Verificar el Deploy

1. Railway desplegará automáticamente cuando hagas push a tu repo
2. O puedes hacer deploy manual desde el dashboard
3. Ve a la URL de tu app
4. Deberías ver la landing page

### 🔟 Crear Usuario de Prueba

1. Ve a `https://tu-app.railway.app/auth/register`
2. Crea una cuenta
3. Inicia sesión
4. Prueba crear un job

## 🐛 Troubleshooting

### Error: "Could not connect to database"
- Verifica que PostgreSQL esté corriendo en Railway
- Verifica que `DATABASE_URL` esté configurada (Railway la añade automáticamente)

### Error: "Redis connection failed"
- Verifica que Redis esté corriendo en Railway
- Verifica que `REDIS_URL` esté configurada (Railway la añade automáticamente)

### Error: "Jobs no se procesan"
- Necesitas ejecutar el worker RQ
- Opción 1: Añade otro servicio en Railway con el mismo Dockerfile pero comando: `python backend/run_worker.py`
- Opción 2: Ejecuta el worker en el mismo contenedor (modifica el script de inicio)

### Frontend no conecta al backend
- Verifica `NEXT_PUBLIC_API_URL` apunta a la URL correcta
- Verifica CORS en `backend/app/config.py`

### Ver logs
- En Railway, ve a tu servicio → **"Deployments"** → Click en el deployment → **"View Logs"**

## 📊 Estructura en Railway

Después de configurar todo, deberías tener:

```
Railway Project
├── 🐳 Tu App (Dockerfile) - Puerto principal
└── 🔴 Redis - Cola de trabajos

Neon (Externo)
└── 🐘 PostgreSQL - Base de datos (serverless)
```

## 🎉 ¡Listo!

Una vez configurado:
1. ✅ PostgreSQL creado y conectado
2. ✅ Redis creado y conectado
3. ✅ Variables de entorno configuradas
4. ✅ API keys añadidas
5. ✅ App desplegada

Tu app debería estar funcionando en `https://tu-app.railway.app`

## 📝 Notas Adicionales

- **Neon**: Plan gratuito generoso (512 MB storage). Perfecto para empezar.
- **Railway**: Plan gratuito con límites. Suficiente para desarrollo y MVP.
- **Redis**: Railway ofrece Redis gratis con límites.
- **Worker**: Para producción, considera ejecutar el worker RQ en un servicio separado para mejor escalabilidad.
- **Costos**: Con Neon + Railway, puedes tener un MVP funcionando completamente gratis.

