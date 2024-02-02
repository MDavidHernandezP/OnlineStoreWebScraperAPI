import requests
from bs4 import BeautifulSoup

def extraer_datos(url):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracción del título del producto
        titulo_tag = soup.find('h1', {'class': 'ui-pdp-title'})
        titulo = titulo_tag.text 

        # Extracción de la calificación
        calificacion_tag = soup.select_one('span.ui-pdp-review__rating')
        calificacion = calificacion_tag.text 

        # Extracción de la cantidad disponible
        disponibilidad_tag = soup.find('span', {'class': 'ui-pdp-buybox__quantity__available'})
        disponibilidad = disponibilidad_tag.text 
        # Extracción del precio
        precio_tag = soup.find('div', {'class': 'ui-pdp-price__second-line'}).find('span', {'class': 'andes-money-amount__fraction'})
        precio = precio_tag.text
        # Extracción de la cantidad de reseñas
        cantidad_resenas_tag = soup.find('span', {'class': 'ui-pdp-review__amount'})
        cantidad_resenas = cantidad_resenas_tag.text

        codigo_producto_tag = soup.find('span', {'class': 'ui-pdp-color--BLUE ui-pdp-family--REGULAR'})
        codigo_producto = codigo_producto_tag.text



# Imprimir el resultado del precio


        # Verificar si algún valor es nulo
        if None in (titulo, calificacion, disponibilidad):
            print("Alguno de los valores es nulo. Repitiendo la solicitud...")
            return None

        # Imprimir los resultados
        print("Título:", titulo)
        print("Calificación:", calificacion)
        print("Cantidad disponible:", disponibilidad)
        print("Precio:", precio)
        print("Cantidad de reseñas:", cantidad_resenas)
        print("Distribuidor:", codigo_producto)

        return titulo, calificacion, disponibilidad

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None
    except Exception as e:
        return None

# URL del producto
url = "https://articulo.mercadolibre.com.mx/MLM-1491295444-chamarra-de-cuero-pu-de-moda-para-mujer-de-otono-e-invierno-_JM#is_advertising=true&position=1&search_layout=grid&type=pad&tracking_id=b307c137-d659-4d0d-9057-e6b91946f548&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=1&ad_click_id=YmI3OTM4ZTQtMjI0YS00NDMwLTgwMWMtNjVlZjI5ZGI3YzUy"

# Realizar solicitudes hasta que no haya valores nulos
while True:
    resultados = extraer_datos(url)
    if resultados:
        break
