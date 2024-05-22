import os
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

client = MongoClient(os.getenv("MONGODB_URI"))
mongodb = client[os.getenv("MONGODB_NAME")]

def create_collections():
    product_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "price", "stock", "created_at"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "Name must be a string and is required",
                    "maxLength": 255,
                },
                "description": {
                    "bsonType": ["string", "null"],
                    "description": "Description can be a string or null",
                },
                "price": {
                    "bsonType": "decimal",
                    "description": "Price must be a decimal and is required",
                    "minimum": 0,
                },
                "category": {
                    "bsonType": ["string", "null"],
                    "description": "Category can be a string or null",
                    "maxLength": 100,
                },
                "stock": {
                    "bsonType": "int",
                    "description": "Stock must be an integer and is required",
                    "minimum": 0,
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Creation date must be a date and is required",
                },
            },
        }
    }

    # Define review validation rules
    review_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["product_id", "user_id", "rating", "comment", "created_at"],
            "properties": {
                "product_id": {
                    "bsonType": "objectId",
                    "description": "Product ID must be an ObjectId and is required",
                },
                "user_id": {
                    "bsonType": "int",
                    "description": "User ID must be an integer and is required",
                },
                "rating": {
                    "bsonType": "int",
                    "description": "Rating must be an integer and is required",
                    "minimum": 1,
                    "maximum": 5,
                },
                "comment": {
                    "bsonType": "string",
                    "description": "Comment must be a string and is required",
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Creation date must be a date and is required",
                },
            },
        }
    }

    # Create or update the collections with the validation rules
    model_list = [
        {
            "collMod": "products",
            "validator": product_validator,
            "validationLevel": "moderate",
        },
        {
            "collMod": "reviews",
            "validator": review_validator,
            "validationLevel": "moderate",
        }
    ]
    for model in model_list:
        try:
            mongodb.create_collection(model["collMod"], validator=model["validator"])
        except CollectionInvalid:
            mongodb.command(model)


if __name__ == "__main__":
    create_collections()
