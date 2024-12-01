from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client.student_management_system

collection_name = db["students"]