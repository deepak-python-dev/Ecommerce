from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status

mongodb = settings.MONGO_DB
reviews_collection = mongodb.get_collection("reviews")


def serialize_review(review):
    review["_id"] = str(review["_id"])
    review["product_id"] = str(review["product_id"])
    return review


class ReviewListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = reviews_collection.find({})
        reviews_list = [serialize_review(review) for review in reviews]
        return Response(reviews_list)

    def post(self, request):
        data = request.data
        data["created_at"] = datetime.now()

        # Your validation code here

        data["product_id"] = ObjectId(data["product_id"])
        reviews_collection.insert_one(data)
        return Response(
            {"message": "Review created successfully"}, status=status.HTTP_201_CREATED
        )


class ReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):
        try:
            review = reviews_collection.find_one({"_id": ObjectId(review_id)})
            if review:
                review = serialize_review(review)
                return Response(review)
            else:
                return Response(
                    {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
                )
        except Exception:
            return Response(
                {"error": "Invalid review ID"}, status=status.HTTP_400_BAD_REQUEST
            )
