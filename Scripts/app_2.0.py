@app.route('/')
def index():
    # --- CUESTIÓN 5: Visualización con Chequeo de Excepciones ---
    try:
        # 1. Intentamos conectar
        conn = get_db_connection()
        
        # Si la conexión falla (es None), lanzamos un error manual
        if conn is None:
            raise Exception("No se pudo establecer conexión con la base de datos.")

        cur = conn.cursor()

        # 2. Ejecutamos la consulta para VISUALIZAR los registros
        cur.execute('SELECT * FROM books ORDER BY id ASC;')
        books = cur.fetchall() # Recuperamos todos los libros

        # 3. Cerramos conexiones (Buenas prácticas)
        cur.close()
        conn.close()

        # 4. Construimos el HTML para mostrar los datos
        # (Esto satisface la parte de "Visualizar los registros")
        html_content = """
        <nav>
            <a href="/">Inicio</a> | 
            <a href="/create">Añadir Libro</a> | 
            <a href="/about">Acerca de</a>
        </nav>
        <hr>
        <h1>Biblioteca (9 Libros)</h1>
        <ul>
        """
        
        for book in books:
            # book[1] es el título, book[2] es el autor
            html_content += f"<li>ID: {book[0]} | <b>{book[1]}</b> escrito por {book[2]}</li>"
        
        html_content += "</ul>"
        return html_content

    except Exception as e:
        # --- AQUÍ ESTÁ EL CHEQUEO DE EXCEPCIONES ---
        # Si algo falla arriba (base de datos apagada, tabla borrada, etc.)
        # el código salta aquí y muestra el error de forma controlada.
        return f"""
        <h1 style='color:red'>Ocurrió un error en el sistema</h1>
        <p>Detalle del error: {e}</p>
        <p>Por favor, verifica que PostgreSQL esté encendido.</p>
        """
