from django.db.models import F
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from .models import Category, Product, CartItem, Order, OrderItem

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "category_name", "name", "slug", "description", "price", "stock", "is_active", "created_at", "updated_at"]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.filter(is_active=True), write_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "subtotal"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")
        if product and quantity and quantity > product.stock:
            raise serializers.ValidationError({"quantity": "Not enough stock available."})
        return attrs

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "price", "quantity", "subtotal"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at", "items"]

class CreateOrderSerializer(serializers.Serializer):
    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        cart_items = list(CartItem.objects.select_related("product").filter(user=user))
        if not cart_items:
            raise serializers.ValidationError("Your cart is empty.")

        for item in cart_items:
            if item.quantity > item.product.stock:
                raise serializers.ValidationError(f"Not enough stock for {item.product.name}.")

        order = Order.objects.create(user=user)
        total = 0
        for item in cart_items:
            product = item.product
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity,
            )
            total += product.price * item.quantity
            product.stock = F("stock") - item.quantity
            product.save(update_fields=["stock"])
        order.total = total
        order.save(update_fields=["total"])
        CartItem.objects.filter(user=user).delete()
        return order
