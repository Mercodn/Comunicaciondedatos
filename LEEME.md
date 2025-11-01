# Configuración del Proyecto

## Requisitos Previos
- Python 3.x instalado
- pip (gestor de paquetes de Python)
- MySQL (XAMPP/WAMP para Windows, Podman para Linux)

## Pasos de Configuración

### 1. Instalar Dependencias
```bash
pip install flask flask-sqlalchemy pymysql python-dotenv
```

### 2. Configuración de la Base de Datos

#### Para Windows (XAMPP/WAMP):
1. Inicia XAMPP/WAMP
2. Copia el archivo `.env.example` y renómbralo a `.env`
3. Modifica el archivo `.env` con estos valores:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=nombre_base_datos
```

#### Para Linux (Podman):
1. El archivo `.env` ya debe tener la configuración correcta:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=nombre_base_datos
```

### 3. Crear la Base de Datos

#### En Windows:
1. Abre phpMyAdmin (http://localhost/phpmyadmin)
2. Crea una nueva base de datos llamada `nombre_base_datos`

#### En Linux:
1. Conéctate al contenedor MySQL:
```bash
podman exec -it tu_contenedor_mysql mysql -u root -proot
```
2. Crea la base de datos:
```sql
CREATE DATABASE nombre_base_datos;
```

### 4. Inicializar las Tablas
En una terminal, ejecuta Python y escribe:
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### 5. Ejecutar la Aplicación
```bash
python app.py
```

## Solución de Problemas

- Si hay problemas de conexión, verifica que:
  - El servidor MySQL esté corriendo
  - Los datos de conexión en `.env` sean correctos
  - El puerto 3306 esté disponible
  - La base de datos exista

- Si hay errores de permisos en Windows:
  - Verifica que el usuario root no tenga contraseña en XAMPP/WAMP
  - O actualiza el archivo `.env` con la contraseña correcta

- Si hay errores de conexión en Linux:
  - Verifica que el contenedor Podman esté corriendo
  - Confirma que el puerto 3306 esté expuesto en el contenedor

## Notas Importantes
- No subas el archivo `.env` al control de versiones
- Mantén actualizado el archivo `.env.example` con la estructura correcta
- Asegúrate de tener todos los permisos necesarios en la base de datos