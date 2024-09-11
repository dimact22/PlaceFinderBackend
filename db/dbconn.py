from pymongo import MongoClient
import os


mongo_uri = os.getenv(
    "MONGO_URL", "mongodb+srv://dimashelichov228:X20XDj6y6MmLs7br@cluster0.mdmmw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
print("MongoDB Verbindungs-URL:", mongo_uri)
client = MongoClient(mongo_uri)

db = client.get_database("user_place")
places = db.get_collection("places")
users = db.get_collection("users")
places.create_index([("location", "2dsphere")])
