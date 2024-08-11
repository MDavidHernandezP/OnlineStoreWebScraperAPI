from fastapi import FastAPI, Request

# Importing the class from the scraper code.
from scraper import Scraper

# Client of the Mongo Database.
from db.client import db_client

app = FastAPI()

# Main route of the API for telling the user how to use it.
@app.get("/")
async def root():
    return {
        "message": "Hello World, Welcome! You have some options of routes to go. (Display all the options for the user.)",
        "routes": {
            "/": "Endpoint root.",
            "/manual/(product)": "Endpoint for writing your product directly on the url.",
            "/scrape": "Endpoint for scraping by passing it a json to the body of the post request for the API.",
            "/data": "Endpoint for looking to all the data as it got scraped into the db.",
            "/featured": "Endpoint for showing valuable insights about the collected data.",
        },

        "example of usage of the route (/scrape)": 
        {
            "product": "Tablet"
        }
    }

# Route for inserting the product to be scraped directly in the url.
@app.get("/manual/{product}")
async def get_product(product: str):

    # Create an instance of the Scraper class.
    scrapy = Scraper(product=product)

    # Run the get_urls method from the Scraper class to get the URLs of each publication of the product.
    await scrapy.get_urls()
    
    # Run the get_data method from the Scraper class to get the data from each URLs of the publications.
    await scrapy.get_data()

    # Returning message for confirmation.
    return {
        "Your product selected was" : product,
        "message": "You could seen the data scraped of your product in the route (/data)."
    }

# Route designed for scraping by passing it a json to the body of the post request.
@app.post("/scrape")
async def scrape(request: Request):

    # Saving the json collected from the post request.
    json = await request.json()

    # Collecting the value from the fiel product.
    product_json = json.get("product")

    # Create an instance of the Scraper class.
    scrapy = Scraper(product=product_json)

    # Run the get_urls method from the Scraper class to get the URLs of each publication of the product.
    await scrapy.get_urls()
    
    # Run the get_data method from the Scraper class to get the data from each URLs of the publications.
    await scrapy.get_data()
    
    return {
        "message": "Scrape data by passing a json to the body of the post request.",
        "Your product selected was": product_json,
        "message": "You could seen the data scraped of your product in the route (/data)."
    }

# Route in the webapp to show all the scraped data.
@app.get("/data")
async def data():

    # This will show all the data from the Mongo DB, but it is limited to 40 cause it's a lot.
    all_urls = list(db_client.monguito.urls.find({}).limit(40))
    all_data = list(db_client.monguito.data.find({}).limit(40))

    # Fixing the type of the ids of the documents in the two collections cause its original type causes errors.
    for doc in all_urls:
        doc['_id'] = str(doc['_id'])

    for doc in all_data:
        doc['_id'] = str(doc['_id'])

    return {
        "message": "These are all the scraped data from the product you choosed (limited to 40 products).",
        "message": "If you want to visualize all the data I highly recommend you to use MongoDB Compass.",
        "urls": all_urls,
        "data": all_data
    }

# Route for showing featured characteristics of the scraped data.
@app.get("/featured")
async def featured():
    
    data_collection = db_client.monguito.data

    # Convert fields to numbers and handle missing or malformed data.
    def to_double(value, default=0.0):
        try:
            return float(value.replace(",", "").replace("% OFF", "").replace("Nuevo  |  +", ""))
        except (ValueError, AttributeError):
            return default

    # Fetch all documents from the collection.
    documents = list(data_collection.find({}))

    # Initialize variables for calculations.
    total_price = total_discount = 0
    total_products = len(documents)
    min_price_product = max_rating_product = max_sales_product = max_discount_product = None
    best_product = None

    for doc in documents:
        price = to_double(doc.get("Price"))
        discount = to_double(doc.get("Discount"))
        sales = to_double(doc.get("Sold Quantity"))
        rating = to_double(doc.get("Rating"))
        
        # Accumulate totals.
        total_price += price
        total_discount += discount

        # Determine min/max products.
        if not min_price_product or price < to_double(min_price_product.get("Price")):
            min_price_product = doc

        if not max_rating_product or rating > to_double(max_rating_product.get("Rating")):
            max_rating_product = doc

        if not max_sales_product or sales > to_double(max_sales_product.get("Sold Quantity")):
            max_sales_product = doc

        if not max_discount_product or discount > to_double(max_discount_product.get("Discount")):
            max_discount_product = doc

        # Determine the best product based on multiple criteria.
        if not best_product or (price < to_double(best_product.get("Price")) and rating > to_double(best_product.get("Rating")) and sales > to_double(best_product.get("Sold Quantity"))):
            best_product = doc

    # Calculate averages.
    avg_price = total_price / total_products if total_products else 0
    avg_discount = total_discount / total_products if total_products else 0

    return {
        "message": "Welcome to the Featured Page, Here we have some presets of valuable insights of the product you selected.",
        "insights": {
            "Average Price": avg_price,
            "Average Discount": avg_discount,
            "Cheaper Product": min_price_product.get("Name") if min_price_product else None,
            "Best Graded Product": max_rating_product.get("Name") if max_rating_product else None,
            "Best Sales Product": max_sales_product.get("Name") if max_sales_product else None,
            "Biggest Discount Product": max_discount_product.get("Name") if max_discount_product else None,
            "Best Product": best_product.get("Name") if best_product else None,
        }
    }