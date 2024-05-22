from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from bson.decimal128 import Decimal128
from decimal import InvalidOperation
from decimal import Decimal
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status

mongodb = settings.MONGO_DB
products_collection = mongodb.get_collection("products")


def validate_product_data(data):
    if "name" not in data or not isinstance(data["name"], str):
        return False, "Invalid or missing 'name'"
    if "price" not in data:
        return False, "Missing 'price'"
    try:
        data["price"] = Decimal128(Decimal(str(data["price"])))
    except (ValueError, TypeError, InvalidOperation):
        return False, "Invalid 'price' format"
    return True, None


def convert_document(document):
    document["_id"] = str(document["_id"])
    document["price"] = str(document["price"])
    document["created_at"] = document["created_at"].isoformat()
    if "updated_at" in document:
        document["updated_at"] = document["updated_at"].isoformat()
    return document


class ProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = products_collection.find({})
        products_list = [convert_document(product) for product in products]
        return Response(products_list)

    def post(self, request):
        data = request.data
        is_valid, error_message = validate_product_data(data)
        if not is_valid:
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        data["created_at"] = datetime.now()
        products_collection.insert_one(data)
        return Response(
            {"message": "Product created successfully"}, status=status.HTTP_201_CREATED
        )


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        try:
            product = products_collection.find_one({"_id": ObjectId(product_id)})
        except Exception:
            return Response(
                {"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        if product:
            return Response(convert_document(product))
        else:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, product_id):
        data = request.data
        is_valid, error_message = validate_product_data(data)
        if not is_valid:
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        data["updated_at"] = datetime.now()
        try:
            result = products_collection.update_one(
                {"_id": ObjectId(product_id)}, {"$set": data}
            )
        except Exception:
            return Response(
                {"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        if result.matched_count > 0:
            return Response({"message": "Product updated successfully"})
        else:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, product_id):
        try:
            result = products_collection.delete_one({"_id": ObjectId(product_id)})
        except Exception:
            return Response(
                {"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        if result.deleted_count > 0:
            return Response({"message": "Product deleted successfully"})
        else:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
