import psycopg2
from flask import Flask, request, url_for, redirect

app = Flask(__name__)

# --- CUESTIÓN 10: SEGURIDAD ---
# Centralizamos las credenciales aquí.
# En un entorno real idealmente usaríamos variables de entorno (os.environ).
DB_HOST = "localhost"
DB_NAME = "flask_db"
DB_USER = "eric"
DB_PASS = "1234"

def get_db_connection():
    """Establece la conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.Error as e:
        # CUESTIÓN 5 y 10: Manejo de errores de conexión
        print(f"Error conectando a la BD: {e}")
        return None

# Variable auxiliar para el menú de navegación (se reutiliza en todas las páginas)
NAV_HTML = """
<nav style="background: #eee; padding: 10px; margin-bottom: 20px;">
    <a href="/">Inicio</a> | 
    <a href="/create">Añadir Libro</a> | 
    <a href="/about">Acerca de</a>
</nav>
<hr>
"""

@app.route('/')
def index():
    # --- CUESTIÓN 5: Visualizar registros con chequeo de excepciones ---
    conn = get_db_connection()
    
    # Verificamos si la conexión falló
    if not conn:
        return "<h1>Error: No hay conexión con la base de datos.</h1>"
    
    try:
        cur = conn.cursor()
        # Recuperamos todos los libros ordenados por ID
        cur.execute('SELECT * FROM books ORDER BY id ASC;')
        books = cur.fetchall()
        cur.close()
        conn.close()

        # Construcción del HTML
        html_content = NAV_HTML + "<h1>Biblioteca</h1><ul>"
        
        for book in books:
            # book[0]=id, book[1]=title, book[2]=author
            html_content += f"""
            <li style="margin-bottom: 10px;">
                ID: {book[0]} | <b>{book[1]}</b> - {book[2]} 
                
                <a href="/edit/{book[0]}" style="margin-left:10px;">[Editar]</a>

                <form action="/delete/{book[0]}" method="POST" style="display:inline;">
                    <button type="submit" onclick="return confirm('¿Borrar?');" style="color:red; margin-left:5px;">
                        Borrar
                    </button>
                </form>
            </li>
            """
        html_content += "</ul>"
        return html_content

    except Exception as e:
        # CUESTIÓN 5: Chequeo de excepciones si falla la consulta SQL
        return f"<h1>Ocurrió un error en el sistema</h1><p>{e}</p>"

@app.route('/about')
def about():
    # --- CUESTIÓN 4: Personalizar la referencia del About ---
    return NAV_HTML + """
    <h1>Acerca del Equipo</h1>
    <p>Práctica realizada por:</p>
    <ul>
        <li><strong>Integrante 1:</strong> Eric [TUS APELLIDOS]</li>
        <li><strong>Integrante 2:</strong> [OTRO NOMBRE O BORRAR]</li>
    </ul>
    """

@app.route('/create', methods=('GET', 'POST'))
def create():
    # --- CUESTIÓN 6: Insertar registros con validación y excepciones ---
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages_num']
        review = request.form['review']

        # Validación de campos nulos (Requisito Cuestión 6)
        if not title or not author or not pages:
            return "<h1>Error:</h1> <p>Título, Autor y Páginas son obligatorios.</p>"

        conn = get_db_connection()
        try:
            cur = conn.cursor()
            # CUESTIÓN 10 (Seguridad): Uso de parámetros (%s) para evitar inyección SQL
            cur.execute('INSERT INTO books (title, author, pages_num, review)'
                        'VALUES (%s, %s, %s, %s)',
                        (title, author, int(pages), review))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            # Chequeo de excepciones en inserción
            return f"Error al insertar en la BD: {e}"

    # Formulario HTML
    return NAV_HTML + """
    <h1>Añadir Libro</h1>
    <form method="post">
        <label>Título:</label> <input type="text" name="title"><br>
        <label>Autor:</label> <input type="text" name="author"><br>
        <label>Páginas:</label> <input type="number" name="pages_num"><br>
        <label>Reseña:</label> <textarea name="review"></textarea><br>
        <button type="submit">Guardar</button>
    </form>
    """

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # --- CUESTIÓN 7: API REST para borrado de un registro por ID ---
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Ejecución segura del borrado
        cur.execute('DELETE FROM books WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error al eliminar: {e}"

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    # --- CUESTIÓN 8: API REST para actualización de un registro por ID ---
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        # Procesar la actualización
        try:
            new_title = request.form['title']
            new_author = request.form['author']
            
            cur.execute('UPDATE books SET title = %s, author = %s WHERE id = %s',
                        (new_title, new_author, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error actualizando: {e}"

    # Mostrar formulario con datos actuales (GET)
    cur.execute('SELECT * FROM books WHERE id = %s', (id,))
    book = cur.fetchone()
    cur.close()
    conn.close()

    if book is None:
        return "Libro no encontrado."

    return NAV_HTML + f"""
    <h1>Editar Libro</h1>
    <form method="post">
        <label>Título:</label> <input type="text" name="title" value="{book[1]}"><br>
        <label>Autor:</label> <input type="text" name="author" value="{book[2]}"><br>
        <button type="submit">Actualizar</button>
    </form>
    """

if __name__ == '__main__':
    # CUESTIÓN 2: Despliegue de la aplicación
    app.run(host='0.0.0.0', port=8080, debug=True)
