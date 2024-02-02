import requests
from bs4 import BeautifulSoup

class MercadoLibreScraper:
    def __init__(self, base_url, keywords, num_pages):
        self.base_url = base_url
        self.keywords = keywords
        self.num_pages = num_pages
        self.total_urls_set = set()

    def scrape_urls(self):
        for keyword in self.keywords:
            urls_set = self._scrape_keyword(keyword)
            self.total_urls_set.update(urls_set)

    def _scrape_keyword(self, keyword):
        urls_set = set()

        for page in range(1, self.num_pages + 1):
            url = f'{self.base_url}{keyword}#D[A:{keyword}]&page={page}'

            try:
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                elements_a = soup.find_all('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')
                for element_a in elements_a:
                    url = element_a.get('href', '')
                    urls_set.add(url)

            except requests.exceptions.RequestException as e:
                print(f"Error while scraping {url}: {e}")

        return urls_set

    def display_total_urls(self):
        total_urls = len(self.total_urls_set)
        print(f"Total URLs capturadas en general: {total_urls}")

if __name__ == "__main__":
    base_url = 'https://listado.mercadolibre.com.mx/'
    ropa_palabras = ['abrigos', 'zapato', 'calcetas']
    num_paginas = 2

    scraper = MercadoLibreScraper(base_url, ropa_palabras, num_paginas)
    scraper.scrape_urls()
    scraper.display_total_urls()
