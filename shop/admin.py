from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image', 'description']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'created_at',
        'updated_at'
    ]
    list_filter = ['name', 'created_at', 'updated_at']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}