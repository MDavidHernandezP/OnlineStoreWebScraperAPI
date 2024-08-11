import asyncio
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import json

# Client of the Mongo Database.
from db.client import db_client

class Scraper:
    def __init__(self, product: str):
        # Create an AsyncHTMLSession object for making asynchronous HTTP requests.
        self.session = AsyncHTMLSession()
        # Store the product name in an instance variable.
        self.product = product.replace(' ', '-').replace('_', '-')



    async def get_urls(self):
        
        # Checking if the collection urls already exists.
        if 'urls' in db_client.monguito.list_collection_names():
            
            # And if exists, delete it.
            db_client.monguito['urls'].drop()
            
            print(f"The collection (urls) has been deleted.")

        # Calling the product that user choosed from the init method.
        self.product = self.product

        """ First loop for looping into the pages of a single search. """

        # Loop through pages, starting from 1, incrementing by 48 up to 1921.
        for page in range(1, 1921, 48):    # Change 1921 to 47 to testing, just to don't have to scrape a massive amount of data for a little test.
            # Construct the URL for each page using the product name and page number.
            main_url = f'https://listado.mercadolibre.com.mx/{self.product}_Desde_{page}_NoIndex_True'
            
            try: 
                # Perform an asynchronous GET request to fetch the page content.
                response = await self.session.get(main_url)

                # Parse the HTML content using BeautifulSoup.
                soup = BeautifulSoup(response.html.html, 'html.parser')
                
                # Find all anchor elements with the specified class.
                elements_a = soup.find_all('a', class_="ui-search-item__group__element ui-search-link__title-card ui-search-link")

                """ Second loop for getting all the urls for the almost 54 products. """
                
                # Loop through each anchor element found.
                for element_a in elements_a:
                    # Extract the URL from the href attribute of the anchor tag.
                    url = element_a.get('href', '')
                    
                    # If the url exists then add it to a dictionary, and then inserting it to the Mongo DB urls collection.
                    if url:
                        url_dict = {"url": url}
                        db_client.monguito.urls.insert_one(url_dict)
                        print(f"URL stored: {url}")
            
            # This error handle is for preventing the running of the API to die if there's a problem scraping the urls.
            except Exception as e:
                print(f"Error fetching URLs: {e}")
        
        print("Url scraping process successfully finished! ")
    


    async def get_data(self):

        # Checking if the collection data already exists.
        if 'data' in db_client.monguito.list_collection_names():

            # And if exists, delete it.
            db_client.monguito['data'].drop()
            
            print(f"The collection (data) has been deleted.")

        # Querying the collection urls for the Mongo DB.
        url_collection = db_client.monguito.urls.find({})

        # For to pass through all the documents of the collection urls.
        for document in url_collection:

            # Getting the values of the url field in the document.
            url = document.get("url")

            # If there is a url in the document then try to make the scraping process.
            if url:
                try:

                    # Perform an asynchronous GET request to fetch the page content of each URL.
                    request_url = await self.session.get(url)
                    
                    # Parse the HTML content using BeautifulSoup.
                    soup = BeautifulSoup(request_url.html.html, 'html.parser')

                    # Extract various details from the product page.
                    name_tag = soup.find('h1', {'class': 'ui-pdp-title'})
                    name = name_tag.text if name_tag else None

                    price_tag = soup.find('div', {'class': 'ui-pdp-price__second-line'}).find('span', {'class': 'andes-money-amount__fraction'})
                    price = price_tag.text if price_tag else None

                    category_tag = soup.find("a", {'class': 'andes-breadcrumb__link'})
                    category = category_tag.text if category_tag else None

                    availability_tag = soup.find('span', {'class': 'ui-pdp-buybox__quantity__available'})
                    availability = availability_tag.text if availability_tag else None

                    sold_tag = soup.find('span', {'class': 'ui-pdp-subtitle'})
                    sold = sold_tag.text if sold_tag else None

                    rating_tag = soup.find('span', {'class': 'ui-pdp-review__rating'})
                    rating = rating_tag.text if rating_tag else None

                    amount_rating_tag = soup.find('span', {'class': 'ui-pdp-review__amount'})
                    amount_rating = amount_rating_tag.text if amount_rating_tag else None

                    product_code_tag = soup.find('span', {'class': 'ui-pdp-color--BLUE ui-pdp-family--REGULAR'})
                    product_code = product_code_tag.text if product_code_tag else None

                    product_number_tag = soup.find('span', {'class': 'ui-pdp-color--BLACK ui-pdp-family--SEMIBOLD'})
                    product_number = product_number_tag.text if product_number_tag else None

                    price_discount_tag = soup.find('div', {'class': 'ui-pdp-price__main-container'}).find('span', {'class': 'andes-money-amount__discount'})
                    price_discount = price_discount_tag.text if price_discount_tag else None

                    amount_fraction_tag = soup.find('span', class_=lambda x: x is not None and 'andes-money-amount__fraction' in x)
                    amount_fraction = amount_fraction_tag.text if amount_fraction_tag else None

                    img_zoom_tags = soup.select('div.ui-pdp-gallery__column .ui-pdp-gallery__wrapper figure.ui-pdp-gallery__figure img[data-zoom]')
                    img_zoom_urls = [img_zoom['data-zoom'] for img_zoom in img_zoom_tags]

                    # Create a dictionary with the extracted data.
                    data_dict = {
                        "_id": document["_id"],    # Using the same id for the respective url document.
                        "Name": name,
                        "Price": price,
                        "Category": category,
                        "Available Units": availability,
                        "Sold Quantity": sold,
                        "Rating": rating,
                        "Number of Ratings": amount_rating,
                        "Product Code": product_code,
                        "Product Number": product_number,
                        "Discount": price_discount,
                        "Original Price": amount_fraction,
                        "Images": img_zoom_urls,
                    }

                    # Inserting the dictionary with all the scraped data of a product into the data collection of the Mongo DB.
                    data_insert = db_client.monguito.data.insert_one(data_dict)

                    # Fixing the type of the id cause it generates problems for the printing in console.
                    data_dict["_id"] = str(data_insert.inserted_id)

                    # Convert the dictionary to a JSON formatted string.
                    json_data = json.dumps(data_dict, indent=2)
                    
                    # Optionally, print or save json_data as needed.
                    print(json_data)

                # This error handle is for preventing the running of the API to die if there's a problem scraping the data of each url.
                except Exception as e:
                    print(f"Error fetching data: {e}")
            else:
                print("No URL found in document.")
        
        print("Data scraping process successfully finished! ")



# Example of usage and testing of the scraper.
async def main():
    # Create an instance of the Scraper class with a product name.
    scraper = Scraper("laptop")
    
    # Run the get_urls method to fetch URLs.
    await scraper.get_urls()
    
    # Run the get_data method to fetch and process data from the URLs.
    await scraper.get_data()

if __name__ == "__main__":
    # Run the main function using asyncio.
    asyncio.run(main())