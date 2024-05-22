from django.core.management.base import BaseCommand
from pymongo.errors import CollectionInvalid
from django.conf import settings

mongodb = settings.MONGO_DB


class Command(BaseCommand):
    help = "Setup Mongodb command"

    def handle(self, *args, **options):
        # Define collection validation rules
        collection_validators = {
            "products": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["name", "price", "stock", "created_at"],
                        "properties": {
                            "name": {"bsonType": "string", "maxLength": 255},
                            "description": {"bsonType": ["string", "null"]},
                            "price": {"bsonType": "decimal", "minimum": 0},
                            "category": {
                                "bsonType": ["string", "null"],
                                "maxLength": 100,
                            },
                            "stock": {"bsonType": "int", "minimum": 0},
                            "created_at": {"bsonType": "date"},
                        },
                    }
                },
                "options": {"validationLevel": "moderate"},
            },
            "reviews": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [
                            "product_id",
                            "user_id",
                            "rating",
                            "comment",
                            "created_at",
                        ],
                        "properties": {
                            "product_id": {"bsonType": "objectId"},
                            "user_id": {"bsonType": "int"},
                            "rating": {"bsonType": "int", "minimum": 1, "maximum": 5},
                            "comment": {"bsonType": "string"},
                            "created_at": {"bsonType": "date"},
                        },
                    }
                },
                "options": {"validationLevel": "moderate"},
            },
        }

        # Create or update collections with validation rules
        for collection_name, validator_data in collection_validators.items():
            try:
                mongodb.create_collection(
                    collection_name, validator=validator_data["validator"]
                )
            except CollectionInvalid:
                # Update collection validator
                mongodb.command(
                    "collMod",
                    collection_name,
                    validator=validator_data["validator"],
                    **validator_data["options"]
                )

        self.stdout.write("Mongo DB setup successfully!!")
