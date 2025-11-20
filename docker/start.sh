#!/bin/bash

# Script para iniciar frontend y backend en Railway

# Iniciar backend en background
cd /app/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Esperar un poco para que el backend inicie
sleep 2

# Iniciar frontend (Next.js en modo production)
cd /app/frontend
npm start -- -p 3000 &
FRONTEND_PID=$!

# Función para cleanup
cleanup() {
    echo "Cerrando servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait
    exit 0
}

# Capturar señales de terminación
trap cleanup SIGTERM SIGINT

# Esperar a que los procesos terminen
wait

