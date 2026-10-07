from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product

class StoreAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="marwan", password="StrongPass123")
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            category=self.category, name="Django Book", slug="django-book",
            description="Backend development book", price="20.00", stock=5
        )

    def test_product_list_is_public(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_login_and_add_to_cart(self):
        token_response = self.client.post("/api/token/", {"username": "marwan", "password": "StrongPass123"})
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")
        response = self.client.post("/api/cart/", {"product_id": self.product.id, "quantity": 2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_checkout_creates_order_and_clears_cart(self):
        token_response = self.client.post("/api/token/", {"username": "marwan", "password": "StrongPass123"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")
        self.client.post("/api/cart/", {"product_id": self.product.id, "quantity": 2}, format="json")
        response = self.client.post("/api/orders/checkout/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total"], "40.00")
