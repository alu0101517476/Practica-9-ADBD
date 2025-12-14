import psycopg2
from flask import Flask

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_HOST = "localhost"
DB_NAME = "flask_db"
DB_USER = "eric"
DB_PASS = "1234"

def get_db_connection():
    """Función para conectar a PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

# --- HTML DE NAVEGACIÓN (Para usar en todas las páginas) ---
NAV_HTML = """
<nav style="background-color: #f8f9fa; padding: 10px; margin-bottom: 20px; border-bottom: 1px solid #ddd;">
    <a href="/" style="text-decoration: none; font-weight: bold; font-size: 1.2em; color: #333;">Inicio (Libros)</a> 
    <span style="margin: 0 10px;">|</span>
    <a href="/about" style="text-decoration: none; font-weight: bold; font-size: 1.2em; color: #007bff;">Acerca de (About)</a>
</nav>
"""

# --- RUTA DE INICIO (Muestra los libros para verificar que todo funciona) ---
@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return "<h1>Error: No se pudo conectar a la base de datos.</h1>"
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM books ORDER BY id;')
    books = cur.fetchall()
    cur.close()
    conn.close()

    # Construimos el HTML de la lista de libros
    html = NAV_HTML
    html += "<h1>Lista de Libros (Biblioteca)</h1>"
    html += "<ul>"
    for book in books:
        # book[1] es Título, book[2] es Autor
        html += f"<li><b>{book[1]}</b> - <i>{book[2]}</i></li>"
    html += "</ul>"
    
    return html

# --- CUESTIÓN 4: PERSONALIZACIÓN DEL ABOUT ---
@app.route('/about')
def about():
    html_content = NAV_HTML + """
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #d64161;">Acerca del Proyecto</h1>
        <p>Esta aplicación ha sido desarrollada como parte de la práctica de <strong>Administración y diseño de bases de datos</strong>.</p>
        
        <h3>Equipo de Desarrollo:</h3>
        <ul style="background-color: #f4f4f4; padding: 20px; border-radius: 5px; list-style-type: none;">
            <li style="margin-bottom: 10px;">
                👤 <strong>Integrante 1:</strong> Eric Bermúdez Hernández
            </li>
            <li style="margin-bottom: 10px;">
                👤 <strong>Integrante 2:</strong> Alba Pérez Rodríguez
            </li>
        </ul>

        <hr>
        <p><em>Grado en Ingeniería Informática - Universidad de La Laguna</em></p>
    </div>
    """
    return html_content

if __name__ == '__main__':
    # Ejecutamos en modo debug para ver errores si los hay
    app.run(host='0.0.0.0', port=8080, debug=True)