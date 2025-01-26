from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Cart, CartItem, Product, Category, Transaction
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
    SimpleCartSerializer,
    UserSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import uuid
from decimal import Decimal
BASE_URL = "http://localhost:5173"
from django.conf import settings
import requests
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
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
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
    except Cart.DoesNotExist:
        return Response({
            'product_exists': False
        })
    except Product.DoesNotExist:
        return Response({
            'product_exists': False
        })
    except Exception as e:
        return Response({'error': str(e)})


@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get('cart_code')
    cart = get_object_or_404(Cart, cart_code=cart_code, paid=False)
    # print(cart)

    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
    """
    Retrieve a cart by its unique cart code if it has not been paid.

    Args:
        - request: The HTTP request object. 
        Expects a 'cart_code' query parameter.

    Returns:
        Response: A JSON response containing the serialized cart data.

    Raises:
        Http404: If no unpaid cart with the given cart code exists.

    Example:
        GET /api/get_cart?cart_code=abc123

        Response:
        {
            "id": 1,
            "cart_code": "abc123",
            "items": [...],
            "paid": false,
            ...
        }
    """
    cart_code = request.query_params.get('cart_code')
    cart = get_object_or_404(Cart, paid=False, cart_code=cart_code)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_quantity(request):
    """
    API view to allow users update quntity of a cart item.
    """
    cartitem_id = request.data.get('item_id')
    quantity = request.data.get('quantity')

    cartitem = get_object_or_404(CartItem, id=cartitem_id)
    quantity = int(quantity)
    cartitem.quantity = quantity
    cartitem.save()
    serializer = CartItemSerializer(cartitem)
    return Response(
        {
            'data': serializer.data,
            'message': "Quantity updated successfully"
        }
    )


@api_view(['POST'])    
def delete_item(request):
    """
    An API view to delete a cart item.
    """
    cart_item_id = request.data.get('item_id')
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    """
    API view function to get username
    """
    username = request.user
    return Response({'username': username.username})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Get User Info
    """
    user = request.user
    seriaizer = UserSerializer(user)
    return Response(
        seriaizer.data
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """
    Initiates a payment through Flutterwave's API.

    This view processes the payment initiation request, creates a new transaction 
    record, and sends a request to Flutterwave's API for payment processing.

    Args:
        request: The HTTP request object containing the cart_code and user info.

    Returns:
        Response: The response object with the payment initiation result.
    """
    if request.user:
        try:
            tx_ref = str(uuid.uuid4())
            cart_code = request.data.get("cart_code")
            cart = Cart.objects.get(cart_code=cart_code)
            user = request.user
            
            amount = sum([item.quantity * item.product.price for item in cart.items.all()])
            tax = Decimal('4.00')
            total_amount = amount + tax
            currency = "NGN"
            
            redirect_url = f"{BASE_URL}/payment-status/"
            
            transaction = Transaction.objects.create(
                ref=tx_ref,
                cart=cart,
                amount = total_amount,
                currency=currency,
                user=user,
                status='pending'                
            )
            
            flutter_wave_payload = {
                "tx_ref": tx_ref,
                'amount': str(total_amount),
                'currency': currency,
                'redirect_url': redirect_url,
                'customer': {
                    'email': user.email,
                    'name': user.username,
                    'phone number': user.phone,
                },
                'configurations': {
                  "session_duration": 5,
                  "max_retry_attempt": 3,
                },
                'customization': {
                    'title': 'VioletteStores Payment'
                }
            }
            
            # Set up the headers for the request.
            headers = {
                "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                'Content-Type': 'application/json'
            }
            
            # Make the API request to flutterwave
            response = requests.post(
                'https://api.flutterwave.com/v3/payments',
                json=flutter_wave_payload,
                headers=headers
            )
            
            # Check if response was succesful.
            if response.status_code == 200:
                return Response(
                    response.json(),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    response.json(),
                    status=response.status_code
                )
        except requests.exceptions.RequestException as e:
            # Log the error and return an error response
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
def payment_callback(request):
    """
    Handles the callback from Flutterwave after a payment is processed.

    This view verifies the payment status by calling Flutterwave's API to ensure
    the transaction was successful and updates the transaction and cart status accordingly.

    Args:
        request: The HTTP request object containing payment status and transaction ID.

    Returns:
        Response: The response object with the result of payment verification.
    """
    status = request.GET.get("status")
    tx_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")

    user = request.user
    
    if status == 'successful':
        # Verify the transaction USING FLUTTERWAVE API
        headers = {
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
        }
        
        response = requests.get(
            f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify',
            headers=headers
        )
        response_data = response.json()

        if response_data['status'] == 'success':
            transaction = Transaction.objects.get(ref=tx_ref)

            # Confirm the transaction details
            if (
                response_data['data']['status'] == 'successful' and
                float(response_data['data']['amount'] == float(transaction.amount)) and
                response_data['data']['currency'] == transaction.currency
                ):
                # Update transaction and cart status to paid
                transaction.status = 'completed'
                transaction.save()
                
                cart = transaction.cart
                cart.paid = True
                cart.user = user
                cart.save()
                
                return Response(
                    {
                        'message': 'Payment Successful!',
                        'subMessage': (
                            'You have successfully made payment for '
                            'the items you purchased 😍'
                        )
                    }
                )
            else:
                # Payment verification failed
                return Response(
                    {
                        'message': 'Payment Verification Failed',
                        "subMessage": "Your payment verification failed, kindly try again."
                    },
                    status=400
                )
        else:
            return Response(
                {
                    'message': (
                        'Failed to verify transaction with Flutterwave.'
                    ),
                    'subMessage': (
                        'We couldn\'t verify your payment, '
                        'use a different payment method'
                    )
                },
                status=400
            )
    else:
        # Payment was not successful
        return Response(
            {
                'message': 'Payment was not successful.'
            },
            status=400
        )