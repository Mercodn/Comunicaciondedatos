from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import json
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
from utils.excel_db import guardar_reporte, cargar_usuarios, verificar_login, registrar_usuario

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Variable global para el GeoJSON
sabana_geojson = None

def cargar_geojson():
    global sabana_geojson
    try:
        geojson_path = 'static/sabana_centro.geojson'
        if not os.path.exists(geojson_path) or os.path.getsize(geojson_path) == 0:
            print(f"⚠️ Archivo {geojson_path} no válido")
            return False
        with open(geojson_path, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            if not contenido:
                print(f"⚠️ Archivo {geojson_path} vacío")
                return False
            sabana_geojson = json.loads(contenido)
            print(f"✅ GeoJSON cargado con {len(sabana_geojson['features'])} municipios")
            return True
    except Exception as e:
        print(f"❌ Error cargando GeoJSON: {e}")
        return False

def obtener_municipio(lat, lng):
    if not sabana_geojson:
        return "Sabana Centro"
    try:
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
        for municipio, bbox in coords_municipios.items():
            if bbox['min_lat'] <= lat <= bbox['max_lat'] and bbox['min_lng'] <= lng <= bbox['max_lng']:
                return municipio
        return "Sabana Centro"
    except Exception as e:
        print(f"Error determinando municipio: {e}")
        return "Sabana Centro"

cargar_geojson()

os.makedirs('logs', exist_ok=True)
handler = RotatingFileHandler('logs/app.log', maxBytes=1024*1024, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reportar", methods=["GET", "POST"])
def reportar():
    if request.method == "GET":
        return render_template("reportar.html")
    try:
        data = request.get_json()
        municipio = obtener_municipio(float(data["latitud"]), float(data["longitud"]))
        guardar_reporte(data["tipo"], data["descripcion"], float(data["latitud"]), float(data["longitud"]), usuario_id=0)
        return jsonify({"mensaje": "Reporte guardado con éxito ✅", "municipio": municipio})
    except Exception as e:
        print(f"Error en reportar: {e}")
        return jsonify({"error": "Error al guardar el reporte"}), 500

@app.route("/lista")
def lista():
    try:
        df = pd.read_excel("reportes.xlsx")
        # Convertir la columna 'Fecha' al formato esperado por el template
        df["Fecha y hora"] = pd.to_datetime(df["Fecha"]).dt.strftime("%d/%m/%Y, %I:%M:%S %p")
        reportes = df.rename(columns={
            "Tipo": "tipo",
            "Descripción": "descripcion",
            "Latitud": "latitud",
            "Longitud": "longitud",
            "Fecha y hora": "fecha_hora"
        }).to_dict(orient="records")
        return render_template("lista.html", reportes=reportes)
    except Exception as e:
        print(f"Error cargando lista: {e}")
        return render_template("lista.html", reportes=[])

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        correo = request.form.get("correo")
        clave = request.form.get("clave")
        usuario = verificar_login(correo, clave)
        if usuario:
            return jsonify({"mensaje": "Login exitoso", "usuario": usuario})
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401
    return render_template("login.html")

@app.route("/dashboard")
def dashboard_view():
    return render_template("dashboard.html")

@app.route("/admin/dashboard")
def admin_dashboard_view():
    return render_template("admin_dashboard.html")

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(500)
def internal_error(e):
    app.logger.exception("Internal server error")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)