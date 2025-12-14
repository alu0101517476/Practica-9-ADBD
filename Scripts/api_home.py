import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# --- CONFIGURACIÓN BD (MyHome) ---
DB_HOST = "localhost"
DB_NAME = "myhome"
DB_USER = "eric"
DB_PASS = "1234"

def get_db_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a MyHome: {e}")
        return None

# --- ESTILOS CSS Y HTML (Para que los botones se vean bonitos) ---
HTML_HEADER = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>MyHome API</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; text-align: center; padding: 40px; }
        h1 { color: #333; margin-bottom: 30px; }
        .menu-container { background: white; max-width: 500px; margin: 0 auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .btn {
            display: block;
            width: 90%;
            margin: 15px auto;
            padding: 15px;
            text-decoration: none;
            color: white;
            font-size: 1.1em;
            border-radius: 5px;
            transition: background 0.3s;
            font-weight: bold;
        }
        /* Colores distintos para diferenciar funciones */
        .btn-blue { background-color: #3498db; }
        .btn-blue:hover { background-color: #2980b9; }
        
        .btn-green { background-color: #2ecc71; }
        .btn-green:hover { background-color: #27ae60; }
        
        .btn-orange { background-color: #e67e22; }
        .btn-orange:hover { background-color: #d35400; }
        
        .btn-purple { background-color: #9b59b6; }
        .btn-purple:hover { background-color: #8e44ad; }

        .btn-dark { background-color: #34495e; }
        .btn-dark:hover { background-color: #2c3e50; }

        .result-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: inline-block; margin-top: 20px;}
        .back-link { display: block; margin-top: 20px; color: #7f8c8d; text-decoration: none; }
    </style>
</head>
<body>
"""

@app.route('/')
def index():
    return HTML_HEADER + """
    <div class="menu-container">
        <h1>🏠 Panel MyHome</h1>
        <p>Selecciona una operación:</p>
        
        <a href="/avg-all" class="btn btn-blue">
            a) Temperatura Media Global
        </a>

        <a href="/max-all" class="btn btn-green">
            b) Temperatura Máxima Global
        </a>

        <a href="/room/1/name" class="btn btn-orange">
            c) Nombre Habitación 1
        </a>

        <a href="/room/1/avg" class="btn btn-purple">
            d) Media Histórica Habitación 1
        </a>

        <a href="/room/1/min-json" class="btn btn-dark">
            e) JSON Mínima Habitación 1
        </a>
    </div>
    </body>
    </html>
    """

# ---------------------------------------------------------
# FUNCIONES DE LA API (Modificadas para tener botón de "Volver")
# ---------------------------------------------------------

@app.route('/avg-all')
def get_average_global():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT AVG(temperature) FROM temperatures;')
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    return HTML_HEADER + f"""
        <div class="result-box">
            <h2>🌡️ Temperatura Media Global</h2>
            <h1 style="color: #3498db;">{round(result, 2)} ºC</h1>
            <a href="/" class="back-link">⬅ Volver al Menú</a>
        </div>
    </body></html>
    """

@app.route('/max-all')
def get_max_global():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT MAX(temperature) FROM temperatures;')
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    return HTML_HEADER + f"""
        <div class="result-box">
            <h2>🔥 Temperatura Máxima</h2>
            <h1 style="color: #e74c3c;">{result} ºC</h1>
            <a href="/" class="back-link">⬅ Volver al Menú</a>
        </div>
    </body></html>
    """

@app.route('/room/<int:room_id>/name')
def get_room_name(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM rooms WHERE id = %s;', (room_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        texto = result[0]
    else:
        texto = "Habitación no encontrada"

    return HTML_HEADER + f"""
        <div class="result-box">
            <h2>🏷️ Nombre de la Habitación {room_id}</h2>
            <h1 style="color: #e67e22;">{texto}</h1>
            <a href="/" class="back-link">⬅ Volver al Menú</a>
        </div>
    </body></html>
    """

@app.route('/room/<int:room_id>/avg')
def get_room_avg(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT AVG(temperature) FROM temperatures WHERE room_id = %s;', (room_id,))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()

    if result:
        val = f"{round(result, 2)} ºC"
    else:
        val = "Sin datos"

    return HTML_HEADER + f"""
        <div class="result-box">
            <h2>📊 Media Histórica (Hab {room_id})</h2>
            <h1 style="color: #9b59b6;">{val}</h1>
            <a href="/" class="back-link">⬅ Volver al Menú</a>
        </div>
    </body></html>
    """

@app.route('/room/<int:room_id>/min-json')
def get_room_min_json(room_id):
    # NOTA: Como esto DEBE devolver JSON puro (según el enunciado e),
    # no podemos meterle HTML ni botones de volver. El navegador mostrará el texto crudo.
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
        SELECT r.name, MIN(t.temperature)
        FROM rooms r
        JOIN temperatures t ON r.id = t.room_id
        WHERE r.id = %s
        GROUP BY r.name;
    """
    cur.execute(query, (room_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        data = {
            "room_id": room_id,
            "room_name": result[0],
            "min_temperature": result[1]
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Habitación no encontrada"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)