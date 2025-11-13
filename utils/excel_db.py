import pandas as pd
from datetime import datetime
import hashlib
import os

# Rutas absolutas para los archivos Excel
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES_PATH = os.path.join(ROOT_DIR, "reportes.xlsx")
USUARIOS_PATH = os.path.join(ROOT_DIR, "usuarios.xlsx")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------- USUARIOS --------------------

def cargar_usuarios():
    if not os.path.exists(USUARIOS_PATH):
        df = pd.DataFrame(columns=["Usuario_ID", "Nombre", "Correo", "Contraseña", "Rol"])
        df.to_excel(USUARIOS_PATH, index=False)
    return pd.read_excel(USUARIOS_PATH)

def registrar_usuario(nombre, correo, clave, rol="usuario"):
    df = cargar_usuarios()
    nuevo_id = int(df["Usuario_ID"].max()) + 1 if not df.empty else 1
    nueva_fila = {
        "Usuario_ID": nuevo_id,
        "Nombre": nombre,
        "Correo": correo,
        "Contraseña": hash_password(clave),
        "Rol": rol
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_excel(USUARIOS_PATH, index=False)

def verificar_login(correo, clave):
    df = cargar_usuarios()
    clave_hash = hash_password(clave)
    usuario = df[(df["Correo"] == correo) & (df["Contraseña"] == clave_hash)]
    return usuario.iloc[0].to_dict() if not usuario.empty else None

# -------------------- REPORTES --------------------

def cargar_reportes():
    if not os.path.exists(REPORTES_PATH):
        df = pd.DataFrame(columns=["ID", "Tipo", "Descripción", "Latitud", "Longitud", "Fecha", "Usuario_ID"])
        df.to_excel(REPORTES_PATH, index=False)
    return pd.read_excel(REPORTES_PATH)

def guardar_reporte(tipo, descripcion, lat, lng, usuario_id):
    df = cargar_reportes()
    nuevo_id = int(df["ID"].max()) + 1 if not df.empty else 1
    nueva_fila = {
        "ID": nuevo_id,
        "Tipo": tipo,
        "Descripción": descripcion,
        "Latitud": lat,
        "Longitud": lng,
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Usuario_ID": usuario_id
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_excel(REPORTES_PATH, index=False)