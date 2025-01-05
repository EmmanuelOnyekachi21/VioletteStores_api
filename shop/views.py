from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, CartItem, Product, Category
from .serializers import (
    CartItemSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer
)
from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(['GET'])
def categories(request):
    """
    API VIEW TO VIEW ALL CATEGORIES
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products(request):
    """
    API VIEW TO VIEW ALL PRODUCTS
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_details(request, slug):
    """
    Retrieve a detailed view of a specific product by its slug.
    This view handles GET requests to return detailed info about a product,
    including similar products based on the same category.

    Args:
        request (Request): The HTTP request object.
        slug (str): The slug (URL-friendly name) of the product to retrieve.

    Returns:
        - Response: A Response object containing the serialized data of the
        product, including the list of similar products.
    """
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
def add_item(request):
    """
    Add a product to the cart.

    This view handles the POST request to add a product to an existing cart or
    create a new cart if one does not exist. It retrieves the cart by its
    cart_code and adds the specified product to the cart as a CartItem. If the
    CartItem already exists, it updates the quantity, otherwise it creates a
    new CartItem with a quantity of 1.

    Args:
        request (HttpRequest): The HTTP request containing the data with
                                'cart_code' and 'product_id' for the product
                                to be added to the cart.

    Returns:
        Response: A JSON response with the CartItem data and a success message
                  or an error message in case of failure.
    """
    try:
        # Extracting the cart_code and product_id from the request data
        cart_code = request.data.get('cart_code')
        product_id = request.data.get('product_id')

        # Retrieve the product using the product_id
        product = get_object_or_404(Product, id=product_id)

        # Retrieve or create the cart using the provided cart_code
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)

        # Retrieve or create the CartItem for the product in the specific cart
        cartItem, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        # Set the quantity of the CartItem to 1
        cartItem.quantity = 1
        cartItem.save()

        # Serialize the CartItem data for the response
        serializer = CartItemSerializer(cartItem)

        # Return a successful response with the serialized data
        return Response(
            {
                'data': serializer.data,
                'message': 'Product Added Successfully',
            },
            status=201
        )
    except Exception as e:
        # Return an error response in case of an exception
        return Response(str(e), status=400)


def product_in_cart(request):
    """
    Check if a product already exists in the cart.
    Takes cart_code and product_id from query parameters.
    Returns a response with product_exist: true or false.
    """
    product_id = request.query_params.get('product_id')
    cart_code = request.query_params.get('cart_code')

    try:
        cart = get_object_or_404(Cart, cart_code=cart_code)
        product = get_object_or_404(Product, id=product_id)
        
        # Check if the product exists in the cart
        cart_item = CartItem.objects.filter(
            cart=cart, product=product
        ).exists()

        return Response(
            {
                'product_exists': cart_item
            }
        )
    except Exception as e:
        return Response(str(e))