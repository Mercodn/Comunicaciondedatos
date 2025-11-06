from pathlib import Path
import sys
from flask_migrate import init as alembic_init, migrate as alembic_migrate, upgrade as alembic_upgrade
from app import app
# from app import db  # app.py ya inicializa db y importa modelos

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations"

def main():
    with app.app_context():
        try:
            if not MIGRATIONS_DIR.exists():
                print("Inicializando migrations (alembic)...")
                alembic_init()
            else:
                print("Directorio migrations ya existe, omitiendo init.")

            print("Generando migración (autodetectando cambios)...")
            alembic_migrate(message="Auto migration")

            print("Aplicando migraciones (upgrade)...")
            alembic_upgrade()

            print("Migraciones aplicadas correctamente.")
        except Exception as e:
            print("Error durante migraciones:", e)
            sys.exit(1)

if __name__ == "__main__":
    main()