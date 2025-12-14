@app.route('/create', methods=('GET', 'POST'))
# Esta función maneja dos cosas: 
    # 1. Mostrar el formulario (GET)
    # 2. Recibir los datos y guardarlos (POST)

def create():
    if request.method == 'POST':
        # Recogemos los datos que escribió el usuario
        title = request.form['title']
        author = request.form['author']
        pages_num = request.form['pages_num']
        review = request.form['review']

        # --- VALIDACIÓN DE CAMPOS NULOS (Requisito de la cuestión) ---
        # Si el título o el autor están vacíos, mostramos error y no guardamos.
        if not title or not author:
            return "<h1>Error:</h1> <p>El Título y el Autor son obligatorios. No se aceptan campos vacíos.</p> <a href='/create'>Intentar de nuevo</a>"

        # --- CHEQUEO DE EXCEPCIONES (Requisito de la cuestión) ---
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            # Insertamos el libro nuevo
            cur.execute('INSERT INTO books (title, author, pages_num, review)'
                        'VALUES (%s, %s, %s, %s)',
                        (title, author, int(pages_num), review))
            conn.commit() # Guardamos cambios
            cur.close()
            conn.close()
            
            # Si todo sale bien, volvemos a la página principal
            return redirect(url_for('index'))
            
        except Exception as e:
            return f"<h1>Error guardando en la Base de Datos</h1> <p>{e}</p>"

    # --- CÓDIGO HTML DEL FORMULARIO ---
    # Esto es lo que ve el usuario cuando entra a la página
    return NAV_HTML + """
    <div style="padding: 20px;">
        <h1>Añadir un Nuevo Libro</h1>
        <form method="post">
            <label><b>Título:</b></label><br>
            <input type="text" name="title" placeholder="Ej: El Hobbit" size="50"><br><br>
            
            <label><b>Autor:</b></label><br>
            <input type="text" name="author" placeholder="Ej: J.R.R. Tolkien" size="50"><br><br>
            
            <label><b>Número de Páginas:</b></label><br>
            <input type="number" name="pages_num" value="100"><br><br>
            
            <label><b>Reseña:</b></label><br>
            <textarea name="review" rows="4" cols="50"></textarea><br><br>
            
            <button type="submit" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer;">
                Guardar Libro
            </button>
        </form>
    </div>
    """

