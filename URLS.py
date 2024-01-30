import requests
from bs4 import BeautifulSoup
import pandas as pd

class MercadoLibreScraper:
    def __init__(self, palabras_clave, base_url, num_paginas):
        self.palabras_clave = palabras_clave
        self.base_url = base_url
        self.num_paginas = num_paginas
        self.df = pd.DataFrame(columns=['id', 'url'])
        self.id_counter = 1

    def scrape_urls(self):
        for palabra in self.palabras_clave:
            urls_set = set()

            for pagina in range(1, self.num_paginas + 1):
                url = f'{self.base_url}{palabra}#D[A:{palabra}]&page={pagina}'

                try:
                    response = requests.get(url)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, 'html.parser')

                    elementos_a = soup.find_all('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')
                    for elemento_a in elementos_a:
                        url = elemento_a.get('href', '')
                        urls_set.add(url)

                except requests.exceptions.RequestException as e:
                    print(f"Error while scraping {url}: {e}")

            self.df = pd.concat([self.df, pd.DataFrame({'id': range(self.id_counter, self.id_counter + len(urls_set)), 'url': list(urls_set)})])
            self.id_counter += len(urls_set)

    def display_df(self):
        print(self.df)

if __name__ == "__main__":
    palabras_clave = ['abrigos', 'zapato', 'calcetas']
    base_url = 'https://listado.mercadolibre.com.mx/'
    num_paginas = 2

    scraper = MercadoLibreScraper(palabras_clave, base_url, num_paginas)
    scraper.scrape_urls()
    scraper.display_df()