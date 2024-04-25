import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import time

class ProductoMercadoLibre:
    def __init__(self, url):
        self.url = url

    async def realizar_solicitud_http(self):
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"Tiempo de solicitud HTTP: {elapsed_time} segundos")
                    return await response.text()
        except aiohttp.ClientError as e:
            print(f"Error al realizar la solicitud: {e}")
            return None

    async def extraer_datos(self):
        html_content = await self.realizar_solicitud_http()

        if html_content:
            # Nuevo inicio para medir el tiempo total

            soup = BeautifulSoup(html_content, 'html.parser')
            img_zoom_tags = soup.select('div.ui-pdp-gallery__column .ui-pdp-gallery__wrapper figure.ui-pdp-gallery__figure img[data-zoom]')
            img_zoom_values = [img_zoom['data-zoom'] for img_zoom in img_zoom_tags]
            titulo_tag = soup.find('h1', {'class': 'ui-pdp-title'})
            titulo = titulo_tag.text if titulo_tag else None
            calificacion_tag = soup.find('span', {'class': 'ui-pdp-review__rating'})
            calificacion = calificacion_tag.text if calificacion_tag else None
            disponibilidad_tag = soup.find('span', {'class': 'ui-pdp-buybox__quantity__available'})
            disponibilidad = disponibilidad_tag.text if disponibilidad_tag else None
            precio_tag = soup.find('div', {'class': 'ui-pdp-price__second-line'}).find('span', {'class': 'andes-money-amount__fraction'})
            precio = precio_tag.text if precio_tag else None
            cantidad_resenas_tag = soup.find('span', {'class': 'ui-pdp-review__amount'})
            cantidad_resenas = cantidad_resenas_tag.text if cantidad_resenas_tag else None
            codigo_producto_tag = soup.find('span', {'class': 'ui-pdp-color--BLUE ui-pdp-family--REGULAR'})
            codigo_producto = codigo_producto_tag.text if codigo_producto_tag else None
            precio_descuento_tag = soup.find('div', {'class': 'ui-pdp-price__main-container'}).find('span', {'class': 'andes-money-amount__discount'})
            precio_descuento = precio_descuento_tag.text if precio_descuento_tag else None
            precio_fraction_span = soup.find('span', class_=lambda x: x is not None and 'andes-money-amount__fraction' in x)
            precio_fraction_span = precio_fraction_span.text if precio_fraction_span else None
            datos_dict = {
                "titulo": titulo,
                "calificacion": calificacion,
                "disponibilidad": disponibilidad,
                "precio": precio,
                "cantidad_resenas": cantidad_resenas,
                "codigo_producto": codigo_producto,
                "descuento": precio_descuento,
                "precio_original": precio_fraction_span,
                "imagenes": img_zoom_values
            }
            json_data = json.dumps(datos_dict, indent=2)
            print(json_data)

            return datos_dict

if __name__ == "__main__":
    start_time_total = time.time()  

    async def main():
        url_sin_descuento = "https://www.mercadolibre.com.mx/xiaomi-pocophone-poco-m5s-dual-sim-256-gb-gris-8-gb-ram/p/MLM23428712?pdp_filters=deal%3AMLM779363-1#polycard_client=homes-korribanSearchTodayPromotions&searchVariation=MLM23428712&position=1&search_layout=grid&type=product&tracking_id=5564c84f-a0a6-4e18-bd05-77253fd449e9&c_id=/home/today-promotions-recommendations/element&c_uid=704bf9ed-1b71-4e4f-ba7f-f65c10b5c392"
        producto = ProductoMercadoLibre(url_sin_descuento)
        await producto.extraer_datos()

    asyncio.run(main())

    end_time_total = time.time()  
    elapsed_time_total = end_time_total - start_time_total
    print(f"Tiempo total del código: {elapsed_time_total} segundos")
