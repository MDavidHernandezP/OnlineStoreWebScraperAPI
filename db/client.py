from pymongo import MongoClient  # Import the MongoClient class from the pymongo library.

# Create an instance of MongoClient to connect to the MongoDB server.
# By default, it connects to the local server at 'localhost' on port 27017.
# This client instance will allow us to interact with the MongoDB database.
try:
    db_client = MongoClient("mongodb://mongodb:27017/")
    db_client.server_info()  # Trying to get information from the server.
    print("Successful connection to MongoDB.")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Justification:
# - MongoClient is essential for establishing a connection to the MongoDB server.
# - This connection is required to perform operations like inserting, querying, updating, and deleting documents in the database.
# - Without this connection, the application wouldn't be able to interact with the MongoDB instance.
# - The MongoClient instance (`db_client`) is used throughout the application to access various collections and perform database operations.

"""
Note from the author: Sorry for the text I just think this script looks so empty, and yeah it could perfectly be in the other code,
but I saw in a video this organization so I thought it was better.
"""