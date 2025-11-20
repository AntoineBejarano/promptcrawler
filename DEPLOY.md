# Guía de Deployment en Railway

Esta guía explica cómo desplegar PromptCrawler en Railway usando Docker.

## Requisitos Previos

- Cuenta en Railway (https://railway.app)
- Repositorio Git (GitHub, GitLab, etc.)
- API Keys:
  - Perplexity API Key
  - OpenAI API Key (opcional)

## Pasos para Deployment

### 1. Preparar el Repositorio

Asegúrate de que todos los archivos estén commiteados:

```bash
git add .
git commit -m "Initial commit"
git push
```

### 2. Crear Proyecto en Railway

1. Ve a https://railway.app y crea un nuevo proyecto
2. Selecciona "Deploy from GitHub repo" (o tu proveedor Git)
3. Conecta tu repositorio

### 3. Configurar Servicios

Railway detectará automáticamente el `Dockerfile` y creará un servicio.

#### Variables de Entorno Necesarias

Añade las siguientes variables de entorno en Railway:

**Base de Datos (PostgreSQL)**
- Añade un servicio PostgreSQL desde Railway (Add Service > Database > PostgreSQL)
- Railway generará automáticamente `DATABASE_URL`

**Redis**
- Añade un servicio Redis desde Railway (Add Service > Database > Redis)
- Railway generará automáticamente `REDIS_URL`

**API Keys**
```
PERPLEXITY_API_KEY=tu-perplexity-api-key
OPENAI_API_KEY=tu-openai-api-key (opcional)
```

**NextAuth**
```
NEXTAUTH_URL=https://tu-app.railway.app
NEXTAUTH_SECRET=genera-un-secret-random-aqui
```

**App URLs**
```
NEXT_PUBLIC_API_URL=https://tu-app.railway.app:8000
NEXT_PUBLIC_APP_URL=https://tu-app.railway.app
BACKEND_URL=http://localhost:8000
```

### 4. Configurar Puertos

El Dockerfile expone dos puertos:
- `8000` para el backend (FastAPI)
- `3000` para el frontend (Next.js)

Railway usará el puerto principal (`PORT`) para el tráfico HTTP. Necesitarás configurar un reverse proxy o usar Railway's native port handling.

**Opción A: Usar un solo puerto (Frontend)**
- Configura Railway para exponer el puerto 3000
- El frontend debería proxy requests al backend

**Opción B: Configurar Nginx (recomendado para producción)**
- Añade Nginx al Dockerfile para hacer reverse proxy

### 5. Configurar Worker

Para procesar jobs, necesitas ejecutar el worker RQ:

1. En Railway, añade otro servicio usando el mismo Dockerfile
2. Configura el comando de inicio como:
   ```
   python -m app.workers.job_worker
   ```

O alternativamente, ejecuta el worker en el mismo contenedor (no recomendado para producción).

### 6. Migraciones de Base de Datos

Ejecuta las migraciones de Alembic antes del primer deploy:

```bash
# En Railway, puedes usar el CLI
railway run alembic upgrade head
```

O crea un script que ejecute las migraciones al inicio (ver `backend/app/main.py` que ya incluye `Base.metadata.create_all`).

### 7. Deploy

Railway desplegará automáticamente cuando hagas push al repositorio.

## Notas Importantes

1. **Puerto**: Railway asigna un puerto dinámico via la variable `PORT`. Asegúrate de que tu aplicación lo respete.

2. **Healthcheck**: El endpoint `/health` está configurado para Railway.

3. **Logs**: Revisa los logs en Railway para debugging.

4. **Costos**: PostgreSQL y Redis en Railway tienen planes gratuitos limitados. Considera usar servicios externos para producción.

## Troubleshooting

### Error de conexión a la base de datos
- Verifica que `DATABASE_URL` esté configurada correctamente
- Asegúrate de que PostgreSQL esté corriendo

### Error de Redis
- Verifica que `REDIS_URL` esté configurada
- Asegúrate de que Redis esté corriendo

### Frontend no conecta al backend
- Verifica `NEXT_PUBLIC_API_URL` apunta al URL correcto
- Revisa CORS settings en `backend/app/config.py`

### Jobs no se procesan
- Verifica que el worker RQ esté corriendo
- Revisa los logs del worker

## Próximos Pasos

- Configurar dominio personalizado
- Añadir Stripe para pagos
- Configurar CI/CD
- Monitoreo y alertas

