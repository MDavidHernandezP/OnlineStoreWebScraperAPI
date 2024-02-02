import requests
from bs4 import BeautifulSoup

def extraer_datos(url, max_intentos_descuento=3):
    while True:
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

            # Intentar extraer el descuento con un límite de intentos
            intento_descuento = 0
            while intento_descuento < max_intentos_descuento:
                # Extracción de la información adicional
                precio_descuento_tag = soup.find('div', {'class': 'ui-pdp-price__main-container'}).find('span', {'class': 'andes-money-amount__discount'})
                precio_descuento = precio_descuento_tag.text if precio_descuento_tag else "None"

                precio_fraction_span = soup.find('span', class_=lambda x: x is not None and 'andes-money-amount__fraction' in x)
                precio_fraction_span = precio_fraction_span.text if precio_fraction_span else "None"

                # Imprimir el resultado del precio con descuento (si está presente)
                if precio_descuento != "None":
                    break  # Salir del bucle interno si la extracción es exitosa
                else:
                    intento_descuento += 1

            # Verificar si algún valor es nulo
            if None in (titulo, calificacion, disponibilidad):
                print("Alguno de los valores es nulo. Repitiendo la solicitud...")
                continue  # Volver a intentar si algún valor es nulo

            # Imprimir los resultados
            print("Título:", titulo)
            print("Calificación:", calificacion)
            print("Cantidad disponible:", disponibilidad)
            print("Precio:", precio)
            print("Cantidad de reseñas:", cantidad_resenas)
            print("Distribuidor:", codigo_producto)
            print("descuento:", precio_descuento)
            print("precio original:", precio_fraction_span )

            return titulo, calificacion, disponibilidad

        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            return None
        except Exception as e:
            
            return None

# URL del producto sin descuento
url_sin_descuento ="https://articulo.mercadolibre.com.mx/MLM-1870380813-chaqueta-casual-para-hombre-negocio-sueter-de-punto-calido-_JM#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb&reco_client=home_navigation-recommendations&reco_item_pos=0&reco_backend_type=function&reco_id=68ae1e63-ab67-4cf4-a77d-b723874a4da8&c_id=/home/navigation-recommendations/element&c_uid=dcf300bc-e426-4127-a2e6-3f5f0fe6958a"

# Realizar solicitudes hasta que no haya valores nulos
while True:
    resultados = extraer_datos(url_sin_descuento)
    if resultados:
        break