from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer is responsible for converting Category model instances
    to and from JSON representations. It includes fields such as `id`,
    `name`, `slug`, `description`, and `image`.

    Fields:
        - id (int): The unique identifier of the category.
        - name (str): The name of the category.
        - slug (str): The slugified version of the category name.
        - description (str): A brief description of the category.
        - image (ImageField): An optional image representing the category.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer is responsible for converting Product model instances
    to and from JSON representations. It includes a nested representation
    of the associated Category model for better context.

    Fields:
        - id (int): The unique identifier of the product.
        - name (str): The name of the product.
        - slug (str): The slugified version of the product name.
        - description (str): A brief description of the product.
        - category (CategorySerializer): A nested serializer representing
                                         the category.
        - price (Decimal): The price of the product.
        - image (ImageField): An optional image representing the product.
        - created_at (datetime): The timestamp when the product
                                 was created (read-only).
        - updated_at (datetime): The timestamp when the product
                                was last updated (read-only).

    Notes:
        - The `category` field is read-only,
        meaning the category details cannot be modified via this serializer.
        - The `created_at` and `updated_at` fields are marked as read-only to
          ensure they are managed exclusively by the system.
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'price',
            'image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
