# 🚀 Subir Proyecto a GitHub

## Pasos para crear el repositorio en GitHub

### 1️⃣ Crear Repositorio en GitHub

1. Ve a https://github.com
2. Inicia sesión
3. Click en **"+"** (arriba a la derecha) → **"New repository"**
4. Nombre del repositorio: `promptcrawler` (o el que prefieras)
5. Descripción: "SaaS que convierte prompts en datasets estructurados usando IA"
6. **IMPORTANTE**: Deja el repositorio **privado** o **público** (según prefieras)
7. **NO marques** "Add a README file" (ya tenemos uno)
8. **NO marques** "Add .gitignore" (ya tenemos uno)
9. Click en **"Create repository"**

### 2️⃣ Conectar y Subir

Después de crear el repositorio, GitHub te mostrará instrucciones. Usa estos comandos:

```bash
# Conectar tu repositorio local con GitHub
git remote add origin https://github.com/TU-USUARIO/promptcrawler.git

# Cambiar a branch main (si GitHub usa main en lugar de master)
git branch -M main

# Subir todo el código
git push -u origin main
```

**Reemplaza** `TU-USUARIO` con tu usuario de GitHub.

### 3️⃣ Verificar

Ve a tu repositorio en GitHub y deberías ver todos los archivos.

---

## ✅ Comandos Listos para Ejecutar

Copia y pega estos comandos (después de crear el repo en GitHub):

```bash
git remote add origin https://github.com/TU-USUARIO/promptcrawler.git
git branch -M main
git push -u origin main
```

---

## 🔐 Si el Repositorio es Privado

Si creaste el repositorio privado, GitHub te pedirá autenticación. Opciones:

1. **Personal Access Token** (recomendado)
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Genera uno con permisos `repo`
   - Úsalo como contraseña cuando git lo pida

2. **GitHub CLI**
   ```bash
   gh auth login
   ```

3. **SSH** (configuración adicional)
   - Genera una SSH key
   - Añádela a GitHub
   - Usa la URL SSH: `git@github.com:TU-USUARIO/promptcrawler.git`

---

## 📝 Nota

Si ya ejecutaste `git init` y `git commit`, solo necesitas:
1. Crear el repo en GitHub
2. Ejecutar los 3 comandos de arriba

¡Listo! 🎉

