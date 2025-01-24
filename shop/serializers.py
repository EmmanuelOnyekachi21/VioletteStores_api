from rest_framework import serializers
from .models import Cart, CartItem, Product, Category
from django.contrib.auth import get_user_model


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


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for each Product detailed page.
    Includes fields for the product itself,
    and dynamically generates a list of similar products.
    """
    related_products = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'price',
            'image', 'related_products'
        ]

    def get_related_products(self, product):
        """
        Retrieves a list of products in same category as the given product,
        excluding the product itself. This method is used to populate the
        `similar_products` field in the serialized output.

        Args:
            product (Product): The product instance being serialized.

        Returns:
            list: A list of serialized similar product objects.
        """
        products = (Product.objects.filter(
            category=product.category
        ).exclude(id=product.id))
        serializer = ProductSerializer(products, many=True)
        return serializer.data


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.

    It's responsible for converting CartItem model instances into
    JSON and vice versa. It includes related Cart and Product information.

    Attributes:
        - cart (CartSerializer): A nested CartSerializer for the related
        Cart model.
        - product (ProductSerializer): A nested ProductSerializer for the
        related Product model.

    Meta:
        model (CartItem): The model to serialize.
        fields (list): The list of fields to include in the serialized data.
    """
    # cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'total', 'quantity']
    
    def get_total(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.

    This serializer is responsible for converting Cart model instances into
    JSON and vice versa, including fields for cart ID, code, and timestamps.

    Meta:
        model (Cart): The model to serialize.
        fields (list): The list of fields to include in the serialized data.
    """
    items = CartItemSerializer(read_only=True, many=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'items', 'sum_total', 'num_of_items', 'created_at', 'modified']

    def get_sum_total(self, obj):
        """
        Get the sum total of products.
        """
        items = obj.items.all()
        return sum([item.product.price * item.quantity for item in items])
    
    def get_num_of_items(self, obj):
        items = obj.items.all()
        return sum([item.quantity for item in items])


class SimpleCartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model that provides a simplified representation.

    Fields:
        - id: The unique identifier of the cart.
        - cart_code: The unique code associated with the cart.
        - number_of_items: The total number of items in the cart,
        calculated dynamically.
    """
    number_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'number_of_items']

    def get_number_of_items(self, obj):
        """
        Calculate the total number of items in the cart.

        Args:
            obj (Cart): The cart instance being serialized.

        Returns:
            int: Total quantity of items in the cart.
        """
        cartItems = CartItem.objects.filter(cart=obj)
        return sum([item.quantity for item in cartItems])
