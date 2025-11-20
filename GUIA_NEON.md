# 🐘 Guía: Configurar Neon (PostgreSQL Serverless)

Neon es un servicio de PostgreSQL serverless perfecto para este proyecto. Es gratis y muy fácil de configurar.

## 🚀 Pasos para Configurar Neon

### 1️⃣ Crear Cuenta en Neon

1. Ve a https://neon.tech
2. Click en **"Sign Up"** (puedes usar GitHub)
3. Confirma tu email si es necesario

### 2️⃣ Crear Proyecto

1. Una vez dentro, click en **"Create Project"**
2. Elige un nombre (ej: "promptcrawler")
3. Selecciona una región cercana a ti
4. Click en **"Create Project"**

### 3️⃣ Obtener Connection String

Neon te mostrará la pantalla de bienvenida con tu connection string.

**Opción 1: Connection String Completa**
```
postgresql://usuario:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require
```

**Opción 2: Desde el Dashboard**
1. Ve a tu proyecto en Neon
2. Click en **"Connection Details"** o **"Connection String"**
3. Selecciona **"Connection string"** (no "Pooled connection")
4. Copia la URL completa

### 4️⃣ Configurar en Railway

1. En Railway, ve a tu servicio
2. Click en **"Variables"**
3. Añade nueva variable:
   - **Nombre**: `DATABASE_URL`
   - **Valor**: Pega tu connection string completa de Neon
4. Guarda

### 5️⃣ Verificar Conexión

La aplicación se conectará automáticamente cuando se despliegue. Las tablas se crearán automáticamente al iniciar.

## 🔍 Ejemplo de Connection String

```
postgresql://neondb_owner:abc123xyz@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Importante**: 
- ✅ Incluye `?sslmode=require` al final
- ✅ Usa la connection string completa (no la pooled)
- ✅ No compartas tu connection string públicamente

## 💡 Ventajas de Neon

- ✅ **Gratis** para empezar (512 MB storage, 0.5 CPU)
- ✅ **Serverless** - se escala automáticamente
- ✅ **Rápido** - conexiones instantáneas
- ✅ **Fácil** - no necesitas gestionar servidores
- ✅ **Backups automáticos**

## 🐛 Troubleshooting

### Error: "Connection refused"
- Verifica que la connection string esté completa
- Asegúrate de incluir `?sslmode=require`
- Verifica que el proyecto en Neon esté activo

### Error: "Authentication failed"
- Verifica que copiaste la connection string completa
- Regenera la password en Neon si es necesario

### Error: "Database does not exist"
- La aplicación creará las tablas automáticamente
- Si persiste, verifica que la connection string apunte a la base de datos correcta

## 📝 Notas

- Neon tiene un plan gratuito generoso para empezar
- Puedes ver tus datos en el dashboard de Neon
- Los backups son automáticos
- Puedes pausar el proyecto cuando no lo uses (ahorra recursos)

## 🔗 Enlaces Útiles

- Dashboard: https://console.neon.tech
- Docs: https://neon.tech/docs
- Status: https://status.neon.tech

