from django.urls import path
from api.views import auth_views, order_views, product_views, review_views

urlpatterns = [
    path("register/", auth_views.RegisterAPIView.as_view(), name="register"),
    path("login/", auth_views.LoginAPIView.as_view(), name="login"),
    path("profile/", auth_views.ProfileAPIView.as_view(), name="profile"),
    path("products/", product_views.ProductListCreateAPIView.as_view(), name="products"),
    path("products/<str:product_id>/", product_views.ProductDetailAPIView.as_view(), name="product-detail"),
    path("orders/", order_views.OrderListCreateAPIView.as_view(), name="orders"),
    path("orders/<str:pk>/", order_views.OrderDetailAPIView.as_view(), name="order-detail"),
    path("reviews/", review_views.ReviewListCreateAPIView.as_view(), name="reviews"),
    path("reviews/<str:review_id>/", review_views.ReviewDetailAPIView.as_view(), name="review-detail"),
]
