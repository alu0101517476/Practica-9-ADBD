@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # --- CUESTIÓN 7: API de Borrado por ID ---
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Ejecutamos el borrado seguro usando el ID recibido
        cur.execute('DELETE FROM books WHERE id = %s', (id,))
        
        conn.commit() # ¡Importante confirmar el cambio!
        cur.close()
        conn.close()
        
        # Al terminar, volvemos a la lista principal
        return redirect(url_for('index'))
        
    except Exception as e:
        # Chequeo de excepciones
        return f"<h1>Error al intentar borrar el libro</h1><p>{e}</p>"
