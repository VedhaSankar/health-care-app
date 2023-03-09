import os
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_pymongo import PyMongo,pymongo
from flask_mongoengine import MongoEngine

load_dotenv()

MONGO_URI       = os.environ.get('MONGO_URI')

# creating a MongoClient object  
client = MongoClient(MONGO_URI)  

# accessing the database  
DB_NAME = 'health-care'
database = client[DB_NAME]


def delete_all_records():

    collection_name = 'users'
    new_collection = database[collection_name]

    new_collection.delete_many({})

def insert_one_user():

    collection_name = 'users'
    new_collection = database[collection_name]

    result = {
            "_id"   : 1,
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "phone_number": "phone_number",
            "password": "password",
            "role": "role"
        }

    x = new_collection.insert_one(result)
    print(x)

def find_by_id(id):

    collection_name = 'users'
    new_collection = database[collection_name]

    x = new_collection.find_one({'_id': id})
    print(x)

def start():

    find_by_id(1)
    # insert_one_user()
    # delete_all_records()

if __name__ == "__main__":
    start()