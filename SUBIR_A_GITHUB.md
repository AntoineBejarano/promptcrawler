# 📤 Subir Proyecto a GitHub - Guía Rápida

## ✅ Lo que ya está hecho

- ✅ Repositorio git inicializado
- ✅ Todos los archivos añadidos
- ✅ Commit inicial creado

## 🎯 Siguiente paso: Crear repositorio en GitHub

### Opción 1: Desde la web de GitHub (Recomendado)

1. **Ve a GitHub**: https://github.com/new
2. **Nombre**: `promptcrawler` (o el que prefieras)
3. **Descripción**: "SaaS que convierte prompts en datasets usando IA"
4. **Visibilidad**: Público o Privado (tu elección)
5. **NO marques nada más** (no README, no .gitignore, no licencia)
6. **Click en "Create repository"**

### Opción 2: Usando GitHub CLI (si lo tienes instalado)

```bash
gh repo create promptcrawler --private --source=. --remote=origin --push
```

## 🔗 Conectar y Subir

**Reemplaza `TU-USUARIO` con tu usuario de GitHub**:

```bash
# Conectar con GitHub
git remote add origin https://github.com/TU-USUARIO/promptcrawler.git

# Cambiar a main (GitHub usa main por defecto)
git branch -M main

# Subir todo
git push -u origin main
```

## 🔐 Autenticación

Si te pide usuario/contraseña:

**Usuario**: Tu usuario de GitHub  
**Contraseña**: Usa un **Personal Access Token** (no tu contraseña de GitHub)

### Crear Personal Access Token:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Selecciona scope: `repo` (todas las opciones de repo)
4. Generate token
5. **Copia el token** (solo se muestra una vez)
6. Úsalo como contraseña cuando git lo pida

## ✅ Verificar

Ve a: `https://github.com/TU-USUARIO/promptcrawler`

Deberías ver todos tus archivos.

## 🚀 Después de subir

Ahora puedes conectar Railway:
1. Ve a Railway → New Project
2. Deploy from GitHub repo
3. Selecciona tu repositorio
4. ¡Railway detectará el Dockerfile automáticamente!

