import psycopg2
from psycopg2 import Error

def inicializar_base_datos():
    conn = None
    try:
        # ---------------------------------------------------------
        # 1. CONEXIÓN CON CHEQUEO DE EXCEPCIONES
        # Intentamos conectarnos. Si falla, saltará al 'except'.
        # ---------------------------------------------------------
        print("Conectando a la base de datos PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            database="flask_db",
            user="eric",      # Asegúrate de que este sea tu usuario creado
            password="1234"   # Asegúrate de que esta sea tu contraseña
        )
        
        cur = conn.cursor()

        # ---------------------------------------------------------
        # 2. CREACIÓN DE LA TABLA (DDL)
        # ---------------------------------------------------------
        # Borramos la tabla si ya existe para empezar limpio
        cur.execute('DROP TABLE IF EXISTS books;')
        
        # Creamos la tabla con la estructura requerida
        create_table_query = '''
        CREATE TABLE books (
            id serial PRIMARY KEY,
            title varchar (150) NOT NULL,
            author varchar (50) NOT NULL,
            pages_num integer NOT NULL,
            review text,
            date_added date DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cur.execute(create_table_query)
        print("Tabla 'books' creada exitosamente.")

        # ---------------------------------------------------------
        # 3. INSERCIÓN DE 9 REGISTROS (DML)
        # Preparamos una lista con los 9 libros requeridos
        # ---------------------------------------------------------
        libros_a_insertar = [
            ('Don Quijote de la Mancha', 'Miguel de Cervantes', 863, 'Obra maestra de la literatura española.'),
            ('El Principito', 'Antoine de Saint-Exupéry', 96, 'Un cuento poético y filosófico.'),
            ('Cien años de soledad', 'Gabriel García Márquez', 417, 'Realismo mágico en su máxima expresión.'),
            ('1984', 'George Orwell', 328, 'Una distopía sobre el control y la vigilancia.'),
            ('Harry Potter y la piedra filosofal', 'J.K. Rowling', 223, 'El inicio de una saga mágica.'),
            ('El Señor de los Anillos', 'J.R.R. Tolkien', 1137, 'Fantasía épica y aventura.'),
            ('Crónica de una muerte anunciada', 'Gabriel García Márquez', 150, 'Una trama atrapante sobre el destino.'),
            ('Fahrenheit 451', 'Ray Bradbury', 158, 'Un futuro donde los libros están prohibidos.'),
            ('Orgullo y Prejuicio', 'Jane Austen', 432, 'Un clásico romántico y social.')
        ]

        # Usamos executemany para insertar todo de golpe (Más eficiente y limpio)
        query_insertar = 'INSERT INTO books (title, author, pages_num, review) VALUES (%s, %s, %s, %s)'
        cur.executemany(query_insertar, libros_a_insertar)
        
        # Guardamos los cambios permanentemente
        conn.commit()
        print(f"¡Éxito! Se han insertado {cur.rowcount} registros en la base de datos.")

        # Cerramos el cursor
        cur.close()

    except (Exception, psycopg2.Error) as error:
        # ---------------------------------------------------------
        # CUMPLIMIENTO DEL REQUISITO: CHEQUEO DE EXCEPCIONES
        # Si algo falla arriba, el código viene aquí en lugar de romperse.
        # ---------------------------------------------------------
        print("¡Error fatal trabajando con PostgreSQL!", error)

    finally:
        # ---------------------------------------------------------
        # CIERRE SEGURO
        # Esto se ejecuta SIEMPRE, haya error o no, para liberar recursos.
        # ---------------------------------------------------------
        if conn:
            conn.close()
            print("La conexión a PostgreSQL se ha cerrado.")

# Ejecutamos la función
if __name__ == "__main__":
    inicializar_base_datos()
