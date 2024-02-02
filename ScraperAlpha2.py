'''Second code, here we'll be scraping the Data of the products in the webpage by passing the URLs of all the 
products from the DB in mySQL and then returning this same Data to the same DB.'''

# Importando cosas del Beautiful Soup 4.
import requests as req
from bs4 import BeautifulSoup
# Importando librería para conectarse con MySQL.
import mysql.connector as sqlcn

# Datos de configuración para conectarse a MySQL.
config = {
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'localhost',
    'database': 'tu_base_de_datos',
    'raise_on_warnings': True
}

# Crear una conexión a la base de datos
conexion = sqlcn.connect(**config)

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Variable ejemplo de las urls.
todas_las_urls = []

# Array para info.
todos_los_nombres = []

# Ciclo for para que itere en las primeras 6 páginas de cada palabra buscada.
for url in todas_las_urls:
    # URL scrapeada guardada en una variable.
    request_url = req.get(url)

    # Haciendo la variable legible para python.
    soup = BeautifulSoup(request_url.text, 'html.parser')
    
    ''' (Toda esta parte debe ser cambiada)
    # Variable para guardar la información de la etiqueta y la clase principal que almacena la información.
    elementos_h1 = soup.find_all('h1',class_='multi--titleText--nXeOvyr')
    for elemento_h1 in elementos_h1:
        nombre = elemento_h1.text.strip()
        todos_los_nombres.append(nombre)
        print(nombre)
    '''
        
todos_los_nombres.sort()
print(len(todos_los_nombres))