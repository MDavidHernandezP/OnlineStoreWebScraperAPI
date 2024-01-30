import requests
from bs4 import BeautifulSoup

class ProductoMercadoLibre:
    def __init__(self, url, max_intentos_descuento=3):
        self.url = url
        self.max_intentos_descuento = max_intentos_descuento

    def realizar_solicitud_http(self):
        while True:
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                return None

    def extraer_datos_principales(self, soup):
        titulo_tag = soup.find('h1', {'class': 'ui-pdp-title'})
        titulo = titulo_tag.text if titulo_tag else None

        calificacion_tag = soup.select_one('span.ui-pdp-review__rating')
        calificacion = calificacion_tag.text if calificacion_tag else None

        disponibilidad_tag = soup.find('span', {'class': 'ui-pdp-buybox__quantity__available'})
        disponibilidad = disponibilidad_tag.text if disponibilidad_tag else None

        precio_tag = soup.find('div', {'class': 'ui-pdp-price__second-line'}).find('span', {'class': 'andes-money-amount__fraction'})
        precio = precio_tag.text if precio_tag else None

        cantidad_resenas_tag = soup.find('span', {'class': 'ui-pdp-review__amount'})
        cantidad_resenas = cantidad_resenas_tag.text if cantidad_resenas_tag else None

        codigo_producto_tag = soup.find('span', {'class': 'ui-pdp-color--BLUE ui-pdp-family--REGULAR'})
        codigo_producto = codigo_producto_tag.text if codigo_producto_tag else None

        return titulo, calificacion, disponibilidad, precio, cantidad_resenas, codigo_producto

    def extraer_descuento(self, soup):
        intento_descuento = 0
        while intento_descuento < self.max_intentos_descuento:
            precio_descuento_tag = soup.find('div', {'class': 'ui-pdp-price__main-container'}).find('span', {'class': 'andes-money-amount__discount'})
            precio_descuento = precio_descuento_tag.text if precio_descuento_tag else None

            precio_fraction_span = soup.find('span', class_=lambda x: x is not None and 'andes-money-amount__fraction' in x)
            precio_fraction_span = precio_fraction_span.text if precio_fraction_span else None

            if precio_descuento:
                return precio_descuento, precio_fraction_span
            else:
                intento_descuento += 1

        return None, None

    def extraer_datos(self):
        while True:
            html_content = self.realizar_solicitud_http()

            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')

                titulo, calificacion, disponibilidad, precio, cantidad_resenas, codigo_producto = self.extraer_datos_principales(soup)

                if None in (titulo, calificacion, disponibilidad):
                    continue

                print("Título:", titulo)
                print("Calificación:", calificacion)
                print("Cantidad disponible:", disponibilidad)
                print("Precio:", precio)
                print("Cantidad de reseñas:", cantidad_resenas)
                print("Distribuidor:", codigo_producto)

                precio_descuento, precio_fraction_span = self.extraer_descuento(soup)

                print("Descuento:", precio_descuento)
                print("Precio original:", precio_fraction_span)

                return titulo, calificacion, disponibilidad

if __name__ == "__main__":
    # URL del producto sin descuento
    url_sin_descuento = "https://www.mercadolibre.com.mx/xiaomi-pocophone-poco-m5s-dual-sim-256-gb-gris-8-gb-ram/p/MLM23428712?pdp_filters=deal%3AMLM779363-1#polycard_client=homes-korribanSearchTodayPromotions&searchVariation=MLM23428712&position=1&search_layout=grid&type=product&tracking_id=5564c84f-a0a6-4e18-bd05-77253fd449e9&c_id=/home/today-promotions-recommendations/element&c_uid=704bf9ed-1b71-4e4f-ba7f-f65c10b5c392"

    # Crear una instancia de la clase ProductoMercadoLibre
    producto = ProductoMercadoLibre(url_sin_descuento)

    # Realizar solicitudes hasta que no haya valores nulos
    while True:
        resultados = producto.extraer_datos()
        if resultados:
            break