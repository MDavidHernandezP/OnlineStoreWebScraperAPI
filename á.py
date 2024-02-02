import requests
from bs4 import BeautifulSoup

def obtener_precio(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra la etiqueta <span> sin clases específicas que contiene 'andes-money-amount__fraction'
        precio_fraction_span = soup.find('span', class_=lambda x: x is not None and 'andes-money-amount__fraction' in x)

        # Obtiene el contenido de texto de la etiqueta encontrada
        precio_texto = precio_fraction_span.get_text(strip=True) if precio_fraction_span else None

        return precio_texto

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL {url}: {e}")
        return None

# URL proporcionada
url_ejemplo = 'https://articulo.mercadolibre.com.mx/MLM-1870380813-chaqueta-casual-para-hombre-negocio-sueter-de-punto-calido-_JM#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb&reco_client=home_navigation-recommendations&reco_item_pos=0&reco_backend_type=function&reco_id=68ae1e63-ab67-4cf4-a77d-b723874a4da8&c_id=/home/navigation-recommendations/element&c_uid=dcf300bc-e426-4127-a2e6-3f5f0fe6958a'

precio = obtener_precio(url_ejemplo)

if precio is not None:
    print("Precio:", precio)
else:
    print("No se pudo obtener el precio.")
