# Importando cosas del Beautiful Soup 4.
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

# Palabras puestas en el buscador: Vestidos, Tacones, Sudaderas, Termos, Coquette.
palabras = ['w/nuevos-lanzamientos-3n82y', 'hombre', 'mujer', 'ninos', 'w/rebajas-3yaep']

# Array para info.
urls = []

# URL de la página web con la busqueda 'Vestidos'.
main_url = f'https://listado.mercadolibre.com.mx/laptops#D[A:laptops,L:undefined]'

# URL scrapeada guardada en una variable.
request_url = session.get(main_url)
request_url.html.render()

# Haciendo la variable legible para python.
soup = BeautifulSoup(request_url.html.html, 'html.parser')

# Variable para guardar la información de la etiqueta y la clase principal que almacena la información.
elementos_a = soup.find_all('a',class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')
for elemento_a in elementos_a:
    # Obtener la URL del atributo href.
    url = elemento_a.get('href', '')
    urls.append(url)
    print(url)
print(len(urls))