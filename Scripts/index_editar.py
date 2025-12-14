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
           # ... (parte anterior de la función index sigue igual) ...
        
        for book in books:
            html_content += f"""
            <li style="margin-bottom: 10px; border-bottom: 1px solid #ccc; padding: 5px;">
                ID: {book[0]} | <b>{book[1]}</b> - {book[2]} 
                
                <a href="/edit/{book[0]}" style="text-decoration: none; color: white; background-color: #008CBA; padding: 5px 10px; margin-left: 10px; border-radius: 3px;">
                   Editar
                </a>

                <form action="/delete/{book[0]}" method="POST" style="display:inline;">
                    <button type="submit" onclick="return confirm('¿Borrar?');" 
                            style="background-color: #ff4444; color: white; border: none; padding: 5px 10px; margin-left: 5px; cursor: pointer; border-radius: 3px;">
                        Borrar
                    </button>
                </form>
            </li>
            """
        
        html_content += "</ul></div>"
        return html_content

    except Exception as e:
        return f"<h1>Error</h1><p>{e}</p>"
