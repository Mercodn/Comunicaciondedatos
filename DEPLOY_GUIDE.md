# 🚀 Guía Rápida de Despliegue - Orden de Implementación

## ✅ PASO 1: Publicar en la Nube (COMENZAR AQUÍ - Más Fácil)

### Opción Recomendada: Render.com (100% Gratis)

**¿Por qué Render?**
- ✅ Plan gratuito generoso (750 horas/mes)
- ✅ Deploy automático desde GitHub
- ✅ HTTPS/SSL incluido
- ✅ Sin tarjeta de crédito
- ✅ Muy fácil de usar

**Pasos:**

1. **Subir código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Preparado para deploy"
   # Crear repo en GitHub.com
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git branch -M main
   git push -u origin main
   ```

2. **Crear cuenta en Render.com:**
   - Ir a https://render.com
   - Sign up con GitHub (más fácil)

3. **Crear Web Service:**
   - Click "New +" → "Web Service"
   - Conectar repositorio de GitHub
   - Seleccionar tu repo
   - Configuración:
     ```
     Name: reportes-incidentes (o el que quieras)
     Region: Singapore (o el más cercano)
     Branch: main
     Runtime: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: gunicorn app:app
     ```
   - Plan: **Free**
   - Click "Create Web Service"

4. **¡Listo!** Tu app estará en: `https://tu-app.onrender.com`

**⏱️ Tiempo estimado: 15-20 minutos**

---

## 🗄️ PASO 2: Base de Datos (Después del Deploy Funcionando)

**Por qué ahora:** El Excel funciona, pero no es ideal para producción.

### Opción: PostgreSQL en Render (Gratis)

1. En Render: "New +" → "PostgreSQL"
2. Name: `reportes-db`
3. Plan: **Free**
4. Anotar las credenciales (Database URL)
5. Modificar `app.py` para usar PostgreSQL con SQLAlchemy

**⏱️ Tiempo estimado: 30-45 minutos (con migración de código)**

---

## 🌐 PASO 3: Dominio Personalizado (Opcional)

1. Comprar dominio en Namecheap, Google Domains, etc.
2. En Render: Settings → Custom Domain
3. Agregar tu dominio
4. Configurar DNS según instrucciones de Render
5. SSL automático (Render lo gestiona)

**⏱️ Tiempo estimado: 10-15 minutos (después de comprar dominio)**

---

## 📧 PASO 5: Mensajería (Más Complejo - Dejar para el Final)

Opciones:
- **Email:** SendGrid, Mailgun (APIs simples)
- **SMS:** Twilio, AWS SNS
- **Notificaciones Push:** Firebase Cloud Messaging

**Recomendación:** Email con SendGrid (más fácil)
- Cuenta gratuita: 100 emails/día
- API simple de usar
- Integrar después de que todo funcione

**⏱️ Tiempo estimado: 1-2 horas (según complejidad)**

---

## 📊 Resumen del Orden

1. ✅ **Deploy en Render** (Más fácil - 20 min)
2. ✅ **Base de datos PostgreSQL** (Necesario - 45 min)
3. ⏭️ **Dominio + SSL** (Opcional - 15 min)
4. ⏭️ **Mensajería** (Complejo - 1-2 horas)

---

## 🆘 Problemas Comunes

### Error: "Module not found"
- Verificar que `requirements.txt` tenga todas las dependencias
- Rebuild en Render

### Error: "Application failed to respond"
- Verificar que el `Procfile` sea correcto: `web: gunicorn app:app`
- Verificar logs en Render Dashboard

### Archivos estáticos no cargan
- Verificar rutas relativas en HTML (`/static/...`)
- Verificar que los archivos estén en el repositorio

---

## ✅ Checklist Pre-Deploy

- [x] `Procfile` creado
- [x] `requirements.txt` actualizado con gunicorn
- [x] `app.py` usa `PORT` de variable de entorno
- [x] `.gitignore` configurado
- [x] Código subido a GitHub
- [ ] Probar localmente con `gunicorn app:app`

