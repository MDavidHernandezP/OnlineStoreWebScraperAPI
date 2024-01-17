# Importando cosas del Beautiful Soup 4.
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time

# Session no sé.
session = HTMLSession()

# Palabras puestas en el buscador: Vestidos, Tacones, Sudaderas, Termos, Coquette.
palabras = ['vestidos', 'tacones', 'sudaderas', 'pantalones', 'coquette']

# Array para info.
urls = []

# Ciclo for para que itere en cada palabra.
for palabra in palabras:
    # Ciclo for para que itere en las primeras 6 páginas de cada palabra buscada.
    for pagina in range(1,5):
        # URL de la página web con la busqueda 'Vestidos'.
        main_url = f'https://es.aliexpress.com/w/wholesale-{palabra}/{pagina}.html?spm=a2g0o.home.search.0'
        # URL scrapeada guardada en una variable.
        request_url = session.get(main_url)
        request_url.html.render()

        # Haciendo la variable legible para python.
        soup = BeautifulSoup(request_url.html.html, 'html.parser')

        # Variable para guardar la información de la etiqueta y la clase principal que almacena la información.
        elementos_a = soup.find_all('a',class_='multi--container--1UZxxHY cards--card--3PJxwBm search-card-item')

        for elemento_a in elementos_a:
            url = elemento_a.get('href', '')
            urls.append(url)
            print(url)
            time.sleep(15)

print(len(urls))