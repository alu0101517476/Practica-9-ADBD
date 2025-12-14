@app.route('/')
def index():
    # --- VISUALIZACIÓN + BOTONES DE BORRAR ---
    try:
        conn = get_db_connection()
        if conn is None:
            return "Error de conexión BD"

        cur = conn.cursor()
        cur.execute('SELECT * FROM books ORDER BY id ASC;')
        books = cur.fetchall()
        cur.close()
        conn.close()

        html_content = NAV_HTML + """
        <div style="padding: 20px;">
            <h1>Biblioteca</h1>
            <ul>
        """
    
        for book in books:
            # book[0] es el ID, book[1] el Título, book[2] el Autor
            # Añadimos un FORMULARIO POST para cada botón de borrar
            html_content += f"""
            <li style="margin-bottom: 10px;">
                ID: {book[0]} | <b>{book[1]}</b> - {book[2]} 
                
                <form action="/delete/{book[0]}" method="POST" style="display:inline;">
                    <button type="submit" onclick="return confirm('¿Estás seguro de querer borrar este libro?');" 
                            style="background-color: #ff4444; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-left: 10px;">
                        Borrar
                    </button>
                </form>
            </li>
            """
        
        html_content += "</ul></div>"
        return html_content
    except Exception as e:
        return f"<h1>Error</h1><p>{e}</p>"
