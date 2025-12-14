@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    # --- CUESTIÓN 8: API de Actualización ---
    conn = get_db_connection()
    cur = conn.cursor()

    # PASO A: Si el usuario dio click a "Guardar Cambios" (Método POST)
    if request.method == 'POST':
        try:
            new_title = request.form['title']
            new_author = request.form['author']
            
            # Ejecutamos el UPDATE seguro
            cur.execute('UPDATE books SET title = %s, author = %s WHERE id = %s',
                        (new_title, new_author, id))
            conn.commit()
            
            cur.close()
            conn.close()
            return redirect(url_for('index'))
            
        except Exception as e:
            return f"<h1>Error al actualizar</h1><p>{e}</p>"

    # PASO B: Si el usuario solo quiere VER el formulario (Método GET)
    # Primero buscamos el libro actual para rellenar los campos
    cur.execute('SELECT * FROM books WHERE id = %s', (id,))
    book = cur.fetchone() # Usamos fetchone() porque solo buscamos UN libro
    cur.close()
    conn.close()

    if book is None:
        return "Libro no encontrado."

    # Renderizamos el formulario con los datos pre-cargados (value="{book[1]}")
    return NAV_HTML + f"""
    <div style="padding: 20px;">
        <h1>Editar Libro: {book[1]}</h1>
        <form method="post">
            <label><b>Título:</b></label><br>
            <input type="text" name="title" value="{book[1]}" size="50"><br><br>
            
            <label><b>Autor:</b></label><br>
            <input type="text" name="author" value="{book[2]}" size="50"><br><br>
            
            <button type="submit" style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; cursor: pointer;">
                Guardar Cambios
            </button>
            <a href="/" style="margin-left: 10px;">Cancelar</a>
        </form>
    </div>
    """
