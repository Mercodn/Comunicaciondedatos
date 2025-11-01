from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
import json

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de MySQL usando variables de entorno
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'reportes_db')
DB_PORT = os.getenv('DB_PORT', '3306')

# Construir URI de conexión
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para los reportes
class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.now)
    municipio = db.Column(db.String(100), nullable=False)

# Variable global para el GeoJSON
sabana_geojson = None

# Cargar el GeoJSON de Sabana Centro con manejo de errores
def cargar_geojson():
    global sabana_geojson
    try:
        geojson_path = 'static/sabana_centro.geojson'
        
        # Verificar si el archivo existe
        if not os.path.exists(geojson_path):
            print(f"⚠️ Archivo {geojson_path} no encontrado")
            return False
            
        # Verificar si el archivo está vacío
        if os.path.getsize(geojson_path) == 0:
            print(f"⚠️ Archivo {geojson_path} está vacío")
            return False
            
        with open(geojson_path, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            
            # Verificar si el archivo tiene contenido
            if not contenido:
                print(f"⚠️ Archivo {geojson_path} no tiene contenido")
                return False
                
            sabana_geojson = json.loads(contenido)
            print(f"✅ GeoJSON cargado correctamente con {len(sabana_geojson['features'])} municipios")
            return True
            
    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error cargando GeoJSON: {e}")
        return False

# Función simplificada para determinar el municipio
def obtener_municipio(lat, lng):
    # Si no hay GeoJSON cargado, retornar mensaje genérico
    if not sabana_geojson:
        return "Sabana Centro"
    
    try:
        # Coordenadas aproximadas de los municipios (ajusta según tus necesidades)
        coords_municipios = {
            'Chía': {'min_lat': 4.8, 'max_lat': 5.0, 'min_lng': -74.1, 'max_lng': -73.9},
            'Cajicá': {'min_lat': 4.9, 'max_lat': 5.0, 'min_lng': -74.1, 'max_lng': -73.9},
            'Zipaquirá': {'min_lat': 5.0, 'max_lat': 5.2, 'min_lng': -74.1, 'max_lng': -73.9},
            'Tabio': {'min_lat': 4.9, 'max_lat': 5.0, 'min_lng': -74.2, 'max_lng': -74.0},
            'Tenjo': {'min_lat': 4.8, 'max_lat': 5.0, 'min_lng': -74.2, 'max_lng': -74.0},
            'Cota': {'min_lat': 4.8, 'max_lat': 5.0, 'min_lng': -74.1, 'max_lng': -74.0},
            'Funza': {'min_lat': 4.7, 'max_lat': 4.8, 'min_lng': -74.2, 'max_lng': -74.1},
            'Mosquera': {'min_lat': 4.7, 'max_lat': 4.8, 'min_lng': -74.2, 'max_lng': -74.1},
            'Madrid': {'min_lat': 4.7, 'max_lat': 4.8, 'min_lng': -74.3, 'max_lng': -74.2},
            'El Rosal': {'min_lat': 4.8, 'max_lat': 5.0, 'min_lng': -74.3, 'max_lng': -74.2},
            'Subachoque': {'min_lat': 4.9, 'max_lat': 5.0, 'min_lng': -74.2, 'max_lng': -74.1},
            'Bojacá': {'min_lat': 4.7, 'max_lat': 4.9, 'min_lng': -74.3, 'max_lng': -74.2}
        }
        
        # Buscar en qué municipio está el punto
        for municipio, bbox in coords_municipios.items():
            if (bbox['min_lat'] <= lat <= bbox['max_lat'] and 
                bbox['min_lng'] <= lng <= bbox['max_lng']):
                return municipio
        
        return "Sabana Centro"
        
    except Exception as e:
        print(f"Error determinando municipio: {e}")
        return "Sabana Centro"

# Cargar el GeoJSON al iniciar la aplicación
cargar_geojson()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reportar", methods=["POST"])
def reportar():
    try:
        data = request.get_json()
        municipio = obtener_municipio(float(data["latitud"]), float(data["longitud"]))
        
        nuevo_reporte = Reporte(
            tipo=data["tipo"],
            descripcion=data["descripcion"],
            latitud=float(data["latitud"]),
            longitud=float(data["longitud"]),
            municipio=municipio
        )
        
        db.session.add(nuevo_reporte)
        db.session.commit()

        return jsonify({"mensaje": "Reporte guardado con éxito ✅", "municipio": municipio})
    except Exception as e:
        db.session.rollback()
        print(f"Error en reportar: {e}")
        return jsonify({"error": "Error al guardar el reporte"}), 500

@app.route("/obtener_reportes")
def obtener_reportes():
    try:
        reportes = Reporte.query.all()
        return jsonify([{
            "tipo": r.tipo,
            "descripcion": r.descripcion,
            "latitud": r.latitud,
            "longitud": r.longitud,
            "fecha_hora": r.fecha_hora.strftime("%d/%m/%Y, %I:%M:%S %p"),
            "municipio": r.municipio
        } for r in reportes])
    except Exception as e:
        print(f"Error obteniendo reportes: {e}")
        return jsonify([])

@app.route("/lista")
def lista():
    try:
        reportes = Reporte.query.all()
        return render_template("lista.html", reportes=[{
            "tipo": r.tipo,
            "descripcion": r.descripcion,
            "latitud": r.latitud,
            "longitud": r.longitud,
            "fecha_hora": r.fecha_hora.strftime("%d/%m/%Y, %I:%M:%S %p"),
            "municipio": r.municipio
        } for r in reportes])
    except Exception as e:
        print(f"Error cargando lista: {e}")
        return render_template("lista.html", reportes=[])

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
