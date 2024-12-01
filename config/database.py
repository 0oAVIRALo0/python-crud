from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
print("MONGO PASSWORD: ", MONGO_PASSWORD)

client = MongoClient(f"mongodb+srv://aviralch30:{MONGO_PASSWORD}@cosmocloud-backend.cnjq0.mongodb.net/?retryWrites=true&w=majority&appName=cosmocloud-backend")

db = client.student_management_system

collection_name = db["students"]