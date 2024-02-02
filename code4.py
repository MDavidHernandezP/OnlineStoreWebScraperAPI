import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuración inicial
url_base = 'https://es.aliexpress.com/w/wholesale-{reemplazo}.html'
palabras_a_buscar = ['coquette', 'vestido', 'tacones', 'sudadera', 'camisa']

# Función para hacer scraping en una página y recorrer las pestañas
def scrape_website(url_base, palabra_cambio):
    try:
        # Cambiar la palabra en la URL
        url_modificada = url_base.replace('{reemplazo}', palabra_cambio)
        print(f"Visitando URL: {url_modificada}")  # Mensaje de depuración

        # Realizar la petición a la primera página
        respuesta = requests.get(url_modificada)
        respuesta.raise_for_status()
        print(f"Cargada la página para '{palabra_cambio}'")  # Mensaje de depuración

        # Procesar todas las páginas/pestañas
        numero_pagina = 1  # Contador para las pestañas
        while True:
            print(f"Procesando pestaña número {numero_pagina} para '{palabra_cambio}'")  # Mensaje de depuración
            
            # Guardar HTML en un archivo
            with open(f'{palabra_cambio}_pagina_{numero_pagina}.html', 'w', encoding='utf-8') as file:
                file.write(respuesta.text)
                print(f"Guardado HTML de la pestaña {numero_pagina} para '{palabra_cambio}' en el archivo")  # Mensaje de depuración

            # Buscar el enlace a la siguiente pestaña/página
            # Aquí deberás ajustar el método de búsqueda para encontrar el enlace correcto a la siguiente página
            siguiente_url = url_modificada+"?page="+str(numero_pagina)
            
            if numero_pagina < 60:

                respuesta = requests.get(siguiente_url)
                respuesta.raise_for_status()
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                print(f"Encontrada la pestaña siguiente para '{palabra_cambio}': {siguiente_url}")  # Mensaje de depuración
                numero_pagina += 1
            else:
                print(f"No se encontraron más pestañas para '{palabra_cambio}'")  # Mensaje de depuración
                break  # No hay más páginas

    except requests.RequestException as e:
        print(f'Error al realizar la petición a {url_modificada}: {e}')

# Ejecutar la función para cada palabra en la lista
for palabra in palabras_a_buscar:
    print(f"Iniciando scraping para '{palabra}'")  # Mensaje de depuración
    scrape_website(url_base, palabra)
