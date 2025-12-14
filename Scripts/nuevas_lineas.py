import os  # <--- NUEVO IMPORT
import psycopg2
from flask import Flask, request, url_for, redirect

app = Flask(__name__)

# --- CUESTIÓN 10: SOLUCIÓN DE SEGURIDAD (CREDENCIALES) ---
# Ya no escribimos la contraseña aquí. La leemos del sistema.
# os.environ.get('NOMBRE_VAR', 'valor_defecto')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'flask_db')
DB_USER = os.environ.get('DB_USER', 'eric')
DB_PASS = os.environ.get('DB_PASS', '1234') # '1234' queda solo como respaldo local