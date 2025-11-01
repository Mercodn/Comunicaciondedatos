# 🚨 Sistema de Reporte de Incidentes Viales - Sabana Centro

Aplicación web para reportar y visualizar incidentes viales en la región de Sabana Centro (Cundinamarca, Colombia).

## 📋 Características

- 🗺️ Mapa interactivo con municipios de Sabana Centro
- 📍 Geolocalización automática o manual
- 📝 Formulario de reporte de incidentes
- 💾 Almacenamiento en Excel (temporal - migrar a BD)
- 📊 Vista de lista de reportes

## 🚀 Despliegue en la Nube (Render.com - GRATIS)

### Opción 1: Render.com (Recomendado - Más Fácil)

1. **Crear cuenta en [Render.com](https://render.com)** (gratis con GitHub)

2. **Preparar repositorio Git:**
   ```bash
   git init
   git add .
   git commit -m "Primer commit"
   git remote add origin [URL_DE_TU_REPOSITORIO]
   git push -u origin main
   ```

3. **En Render.com:**
   - Click en "New +" → "Web Service"
   - Conectar tu repositorio de GitHub
   - Configuración:
     - **Name:** `reportes-incidentes` (o el que prefieras)
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
   - Click "Create Web Service"

4. **Listo!** Tu app estará en: `https://tu-app.onrender.com`

### Opción 2: Railway.app (Alternativa)

1. Crear cuenta en [Railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Seleccionar tu repositorio
4. Railway detecta automáticamente Flask y despliega

## 🗄️ Próximos Pasos: Base de Datos

Después del deploy, migrar de Excel a PostgreSQL:
- Render incluye PostgreSQL gratuito
- Modificar `app.py` para usar SQLAlchemy
- Más estable y escalable

## 📦 Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

La app estará en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración para deploy
├── templates/            # Plantillas HTML
│   ├── index.html        # Página principal con mapa
│   └── lista.html        # Lista de reportes
├── static/               # Archivos estáticos
│   ├── sabana_centro.geojson  # Datos geográficos
│   ├── script.js         # JavaScript del mapa
│   └── styles.css        # Estilos
└── data/                 # Datos (no incluir en Git)
    └── reportes_incidentes.xlsx
```

## 🔧 Variables de Entorno

- `PORT`: Puerto del servidor (automático en Render/Railway)

## ⚠️ Nota Importante

- El archivo Excel se crea automáticamente si no existe
- Para producción, migrar a base de datos PostgreSQL
- El GeoJSON se carga desde `static/sabana_centro.geojson`

