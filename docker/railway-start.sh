#!/bin/bash

# Script optimizado para Railway
# Railway expone un solo puerto (PORT), así que usamos reverse proxy
# Backend en puerto 8000, Frontend en puerto 3000

# Iniciar backend en background
cd /app/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Esperar a que el backend inicie
sleep 3

# Iniciar frontend en background
cd /app/frontend
npm start -- -p 3000 &
FRONTEND_PID=$!

# Usar nginx o similar para reverse proxy si es necesario
# Por ahora, Railway debería poder manejar múltiples puertos
# O usar el puerto principal para frontend y proxy a backend

# Función de cleanup
cleanup() {
    echo "Cerrando servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait
    exit 0
}

# Capturar señales
trap cleanup SIGTERM SIGINT

# Esperar indefinidamente
while true; do
    sleep 60
    # Verificar que los procesos estén corriendo
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "Backend process died, exiting..."
        cleanup
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "Frontend process died, exiting..."
        cleanup
    fi
done

