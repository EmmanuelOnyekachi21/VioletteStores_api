from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.

    This class customizes the Django admin interface for the Category model,
    providing options for displaying, searching, and managing categories.

    Attributes:
        list_display (list): Defines fields to show in the list view of
                             categories.
        search_fields (list): Specifies the fields to enable search function.
        prepopulated_fields (dict): Automatically populates the slug field
        list_editable (list): Fields that can be edited directly
                              in the list view.
    """
    list_display = ['name', 'id', 'slug', 'image', 'description']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.

    This class customizes the Django admin interface for the Product model,
    allowing better management of product details.

    Attributes:
        list_display (list): Fields to display in the list view of products.
        list_filter (list): Fields to filter products by in admin interface.
        list_editable (list): Fields that can be edited directly in interface
        prepopulated_fields (dict): Automatically populates the slug field.
    """
    list_display = [
        'name',
        'category',
        'slug',
        'price',
        'id',
        # 'created_at',
        # 'updated_at'
    ]
    list_filter = ['name', 'created_at', 'updated_at']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}
