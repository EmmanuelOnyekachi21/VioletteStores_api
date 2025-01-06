"""
URL configuration for shop app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('product/<slug:slug>/', views.product_details, name='product_details'),
    path('add_item/', views.add_item, name='add_item'),
    path('product_in_cart/', views.product_in_cart, name='product_in_cart'),
    path('get_cart_stat/', views.get_cart_stat, name='get_cart_stat'),
]
