# PromptCrawler -- De idea a SaaS en 7 días

> **Tagline**:\
> *"Convierte cualquier prompt en un dataset real de la web."*

Este documento es una guía para construir y desplegar en **1 semana** un
MVP funcional de **PromptCrawler**, un SaaS que:

-   Acepta un **prompt en lenguaje natural**
-   Usa **Perplexity + Crawl4AI + LLMs** para:
    -   Descubrir fuentes
    -   Crawlear webs
    -   Extraer datos estructurados
-   Devuelve un **dataset descargable (JSON/CSV)**

------------------------------------------------------------------------

## 0. Alcance del MVP (importante)

El MVP **no va a escanear todo internet**.\
Pero **sí va a funcionar muy bien** para prompts del estilo:

-   "Dame una lista de clubes de cannabis en Sudáfrica."\
-   "Extrae emails de empresas de IA en España."\
-   "Lista escuelas de surf en Portugal con web y ubicación."

El objetivo en 1 semana:

-   ✅ Registro/login
-   ✅ Dashboard simple
-   ✅ Crear "jobs" a partir de prompts
-   ✅ Proceso asíncrono:
    -   prompt → descubrimiento de URLs (Perplexity)
    -   scraping → Crawl4AI
    -   extracción → LLM (OpenAI / Perplexity)
-   ✅ Ver el resultado en tabla
-   ✅ Descargar JSON/CSV
-   ✅ Pricing básico / página de pricing
-   ✅ Deploy en producción

------------------------------------------------------------------------

## 1. Nombre, branding y propuesta de valor

### Nombre

-   **PromptCrawler**

### Tagline

> "De prompt a dataset estructurado, directamente desde la web."

### Elevator pitch

> PromptCrawler es una plataforma que convierte cualquier pregunta en un
> dataset real, buscado y scrapeado desde la web.\
> Es como un "scraper inteligente" guiado por IA: tú escribes lo que
> quieres, y nosotros descubrimos fuentes, las crawleamos y te
> devolvemos datos limpios y estructurados.

------------------------------------------------------------------------

## 2. Stack técnico recomendado

### Frontend

-   Next.js (React, TypeScript)
-   Tailwind CSS
-   NextAuth (Auth.js)
-   shadcn/ui

### Backend

-   FastAPI (Python)
-   PostgreSQL
-   Redis + RQ/Celery
-   Crawl4AI
-   Perplexity API
-   OpenAI API (opcional)

### Hosting

-   Frontend: Vercel
-   Backend: Railway / Render / Fly.io
-   DB: Railway / Neon / Supabase
-   Redis: Upstash

------------------------------------------------------------------------

## 3. Modelo de datos (PostgreSQL)

Tablas: - users - projects - jobs - job_results - job_sources

------------------------------------------------------------------------

## 4. Algoritmo / pipeline

1.  Usuario envía prompt.\
2.  Job creado (`pending`).\
3.  Worker:
    -   Perplexity → URLs
    -   Crawl4AI → Markdown
    -   LLM extractor → JSON\
4.  Job almacenado\
5.  Usuario descarga dataset

------------------------------------------------------------------------

## 5. API

### POST `/api/jobs`

Crea un job.

### GET `/api/jobs`

Lista jobs.

### GET `/api/jobs/{id}`

Detalle.

### GET `/api/jobs/{id}/results?format=json|csv`

------------------------------------------------------------------------

## 6. Frontend (Next.js)

### `/`

Landing con: - Hero - Cómo funciona - Pricing - CTA

### `/dashboard`

-   Crear job
-   Lista de jobs

### `/jobs/[id]`

-   Tabla
-   Descargas JSON/CSV

------------------------------------------------------------------------

## 7. Pricing

### Free

-   5 jobs / mes\
-   200 items / job

### Pro (€29)

-   100 jobs / mes\
-   2000 items / job\
-   API

### Team (€99)

-   500 jobs / mes\
-   10k items / job

------------------------------------------------------------------------

## 8. Plan de 7 días

### Día 1

Estructura + repos + landing.

### Día 2

Auth + dashboard.

### Día 3

Jobs + cola.

### Día 4

Perplexity.

### Día 5

Crawl4AI + extracción.

### Día 6

UI resultados + descargas.

### Día 7

Deploy + tests.

------------------------------------------------------------------------

## 9. Legal mínimo

-   El usuario es responsable del uso.
-   Puede haber limitaciones por ToS de terceros.

------------------------------------------------------------------------

## 10. Próximos pasos

-   Stripe
-   Jobs recurrentes
-   Filtros avanzados
-   Creditos por uso

------------------------------------------------------------------------

## 11. Resumen

MVP desplegable en 7 días con: - Perplexity - Crawl4AI - LLM
extraction - Dashboard + jobs - Export JSON/CSV



promptcrawler/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── workers/
│   │   └── services/
│   ├── requirements.txt
│
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── app/...
│
├── docker/
│   ├── Dockerfile
│
└── README.md
