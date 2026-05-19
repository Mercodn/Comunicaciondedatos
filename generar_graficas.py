import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta absoluta al archivo Excel
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTES_PATH = os.path.join(ROOT_DIR, "reportes.xlsx")
IMG_DIR = os.path.join(ROOT_DIR, "static", "img")
os.makedirs(IMG_DIR, exist_ok=True)

# Cargar datos
df = pd.read_excel(REPORTES_PATH)

# Normalizar columnas si vienen en minúsculas
df.rename(columns={"latitud": "Latitud", "longitud": "Longitud"}, inplace=True)

# -------------------- Gráfica por tipo --------------------
plt.figure(figsize=(8, 5))
df["Tipo"].value_counts().plot(kind="bar", color="#3498db")
plt.title("Reportes por tipo")
plt.xlabel("Tipo")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "reportes_por_tipo.png"))
plt.close()

# -------------------- Gráfica por día --------------------
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Día"] = df["Fecha"].dt.date
plt.figure(figsize=(8, 5))
df["Día"].value_counts().sort_index().plot(kind="line", marker="o", color="#2ecc71")
plt.title("Reportes por día")
plt.xlabel("Fecha")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "reportes_por_dia.png"))
plt.close()

# -------------------- Gráfica por municipio (si existe) --------------------
if "Municipio" in df.columns:
    plt.figure(figsize=(8, 5))
    df["Municipio"].value_counts().plot(kind="bar", color="#e67e22")
    plt.title("Reportes por municipio")
    plt.xlabel("Municipio")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, "reportes_por_municipio.png"))
    plt.close()

print("✅ Gráficas generadas en static/img/")
print("Columnas disponibles:", df.columns.tolist())
print("Primeras filas:")
print(df.head())

# -------------------- Gráfica de total de reportes por usuario --------------------
USUARIOS_PATH = os.path.join(ROOT_DIR, "usuarios.xlsx")
df_usuarios = pd.read_excel(USUARIOS_PATH)

# Contar reportes por Usuario_ID
conteo = df["Usuario_ID"].value_counts().rename_axis("Usuario_ID").reset_index(name="Cantidad")

# Unir con nombres
df_usuarios = df_usuarios[["Usuario_ID", "Nombre"]]
df_merged = pd.merge(conteo, df_usuarios, on="Usuario_ID", how="left")

# Graficar
plt.figure(figsize=(8, 5))
df_merged.set_index("Nombre")["Cantidad"].plot(kind="bar", color="#9b59b6")
plt.title("Total de reportes por usuario")
plt.xlabel("Usuario")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "reportes_por_usuario.png"))
plt.close()