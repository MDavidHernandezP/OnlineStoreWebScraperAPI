import requests
from bs4 import BeautifulSoup
import mysql.connector

# MySQL database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'new_schema',
}

# Lista de palabras relacionadas con ropa
ropa_palabras = ['abrigos', 'zapato','calcetas']

# Base URL común
base_url = 'https://listado.mercadolibre.com.mx/'

# Número de páginas a rastrear
num_paginas = 2

# Establecer la conexión a MySQL
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Crear la tabla 'ropa' con la columna 'id'
    create_table_query = """
    CREATE TABLE IF NOT EXISTS ropa (
        id INT AUTO_INCREMENT PRIMARY KEY,
        urls VARCHAR(3000)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Bucle para cambiar de palabras clave
    for palabra in ropa_palabras:
        # Conjunto para almacenar URLs únicas
        urls_set = set()

        # Bucle para cambiar de páginas
        for pagina in range(1, num_paginas + 1):
            # Construir la URL para la palabra y la página actual
            url = f'{base_url}{palabra}#D[A:{palabra}]&page={pagina}'

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises an HTTPError for bad responses

                soup = BeautifulSoup(response.text, 'html.parser')

                elementos_a = soup.find_all('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')
                for elemento_a in elementos_a:
                    url = elemento_a.get('href', '')
                    urls_set.add(url)

            except requests.exceptions.RequestException as e:
                print(f"Error while scraping {url}: {e}")

        # Insertar las URLs únicas en la tabla 'ropa'
        for unique_url in urls_set:
            # Insertar la URL en la tabla 'ropa'
            insert_query = "INSERT INTO ropa (urls) VALUES (%s)"
            cursor.execute(insert_query, (unique_url,))

except mysql.connector.Error as err:
    print(f"MySQL error: {err}")

finally:
    # Commit de los cambios y cerrar la conexión
    if conn.is_connected():
        conn.commit()
        conn.close()