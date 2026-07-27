from pathlib import Path
import os

PROYECTO = "FlightHunterAI"

carpetas = [
    "",
    "app",
    "app/api",
    "app/core",
    "app/models",
    "app/services",
    "app/services/providers",
    "app/database",
    "app/utils",
    "app/templates",
    "app/static",
    "tests",
    "logs",
    "data",
    "docs"
]

archivos = {
    "README.md": "# FlightHunterAI\n",
    ".gitignore": """venv/
__pycache__/
*.pyc
.env
logs/
data/*.db
""",
    ".env": "",
    "requirements.txt": "",
    "app/main.py": "",
    "app/config.py": "",
    "app/database/database.py": "",
    "app/models/vuelo.py": "",
    "app/services/buscador.py": "",
    "app/services/providers/__init__.py": "",
    "app/utils/helpers.py": "",
}

print(f"\nCreando proyecto {PROYECTO}...\n")

for carpeta in carpetas:
    ruta = Path(PROYECTO) / carpeta
    ruta.mkdir(parents=True, exist_ok=True)

for archivo, contenido in archivos.items():
    ruta = Path(PROYECTO) / archivo
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

print("✅ Estructura creada correctamente.")
print("\nSiguiente paso:")
print(f"cd {PROYECTO}")
print("python -m venv venv")