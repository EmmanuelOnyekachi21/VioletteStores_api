from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer
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
        Response: A Response object containing the serialized data of the product,
                  including the list of similar products.
    """
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)