
[![Python](https://img.shields.io/badge/python-3.12.1-red.svg)](https://www.python.org/)
[![Postman](https://img.shields.io/badge/Postman-v10.8.1-orange.svg)](https://www.postman.com/)
[![Download Postman](https://img.shields.io/badge/Download-Postman-yellow.svg)](https://www.postman.com/downloads/)
[![Docker](https://img.shields.io/badge/Docker-v20.10.17-purple.svg)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-v20.10.17-green.svg)](https://hub.docker.com/)
[![Docker Docs](https://img.shields.io/badge/Docker%20Docs-v20.10.17-gold.svg)](https://docs.docker.com/)

# Dockerized Async Web Scraper with Flask API

This project implements a Dockerized environment for an asynchronous web scraper using Python and Flask. The scraper is designed to extract specific data from Mercado Libre product pages.

## Code Overview

### 1. `requirements.txt`

Contains the required Python dependencies for the project, ensuring a consistent environment.

### 2. `Dockerfile`

Configures the Docker image by setting up the working directory, copying the necessary files, and installing dependencies. It exposes port 6000 and specifies the command to run the Flask application.

### 3. `docker-compose.yml`

Defines the Docker services, specifying the build context, port binding, and volume mapping. Additionally, it sets the Flask app environment variable.

### 4. `ASICROSCRAPPER.py`

An asynchronous web scraper implemented in Python using `aiohttp` and `BeautifulSoup`. It extracts various product details from Mercado Libre given a product URL.

### 5. `app.py`

The Flask application that serves as the API endpoint. It includes routes for scraping data and additional endpoints for general use.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoint](#api-endpoint)
- [Examples](#examples)
- [Contributions](#contributions)
- [Contributors](#contributors)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone -b master git@github.com:MDavidHernandezP/WSMercadoLibre.git
    cd "the proyect directory"
    ```

2. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

## Usage

After successful installation, the Flask application will be accessible, use [postman](https://www.postman.com/downloads/), once you are there you will see a search bar where you will put the direction `http://localhost:6000` , then "/" and the name of the endpoint below, 
make sure the method is correct, once it connects you will see a menu below, where you could see the button "body", press it, and below that press the button "raw", and put the json with link and finally just press it again to send it.

## API Endpoint

- **Endpoint:** `/scrape`
- **Method:** POST
- **Request Format:**

    ```json
    {
        "url": "https://www.mercadolibre.com.mx/tu-producto"
    }
    ```

- **Response Format:**

    ```json
    {
        "message": "Datos obtenidos con éxito!",
        "data": {
            "titulo": "...",
            "calificacion": "...",
            "disponibilidad": "...",
            "precio": "...",
            "cantidad_resenas": "...",
            "codigo_producto": "...",
            "descuento": "...",
            "precio_original": "...",
            "imagenes": ["..."]
        }
    }
    ```
![](https://global.discourse-cdn.com/getpostman/original/2X/d/de461711cd62edb4f7e8f170c6a21aa0fe304fea.png)
## Contributions

1. Fork the project.
2. Create a branch (`git checkout -b feature/nueva-caracteristica`).
3. Commit your changes (`git commit -am 'Añadir nueva característica'`).
4. Push the branch (`git push origin feature/nueva-caracteristica`).
5. Open a pull request.

## Contributors

1. HERNÁNDEZ PANTOJA MARIO DAVID
2. HERNÁNDEZ WIDMAN GERARDO
3. JANETH GUADALUPE VALDIVIA PEREZ
4. ESTHER GUADALUPE APAZA HACHO
5. SERGIO JOHANAN BARRERA CHAN

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley) file for details.

---


