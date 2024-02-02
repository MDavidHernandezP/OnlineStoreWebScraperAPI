import requests
from bs4 import BeautifulSoup
import os

# Inicializar variables
search_url = "https://www.example.com/search?page={}&q={}"
images_directory = "images"
already_downloaded_images = []

# Crear el directorio donde se guardarán las imágenes si aún no existe
if not os.path.exists(images_directory):
    os.makedirs(images_directory)

# Lista de palabras de búsqueda
palabras_a_buscar = ["word1", "word2", "word3"]

# Recorrer cada página de la búsqueda
for word in palabras_a_buscar:
    for page in range(1, 61):
        # Realizar la solicitud HTTP GET para obtener el contenido de la página
        response = requests.get(search_url.format(page, word))
        content = response.content

        # Crear un objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(content, "html.parser")

        # Encontrar todas las imágenes de la página
        for img in soup.find_all("img"):
            image_url = img.get("src")

            # Verificar si la imagen ya ha sido descargada
            if image_url not in already_downloaded_images:
                # Descargar la imagen y guardarla en el directorio 'images_directory'
                response = requests.get(image_url)
                image_name = os.path.basename(image_url)
                with open(os.path.join(images_directory, image_name), "wb") as file:
                    file.write(response.content)

                # Agregar la URL de la imagen a la lista de imágenes ya descargadas
                already_downloaded_images.append(image_url)

        # Si la búsqueda se completa en una página anterior, se detiene el bucle
        if page > 5 and already_downloaded_images[-10:] == already_downloaded_images[-5:]:
            break