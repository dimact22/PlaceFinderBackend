from pymongo import MongoClient
import os


mongo_uri = os.getenv(
    "MONGO_URL", "...")
print("MongoDB Verbindungs-URL:", mongo_uri)
client = MongoClient(mongo_uri)

db = client.get_database("user_place")
places = db.get_collection("places")
users = db.get_collection("users")
places.create_index([("location", "2dsphere")])
