from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    This class customizes the display and functionality of the CustomUser model
    within the Django admin interface.

    Attributes:
        - add_fieldsets (tuple): Defines the fields and layout for adding new
        users in the admin interface.
    """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2', 'city', 'state', 'address',
                'phone', 'is_staff', 'is_active'
            )
        }),
    )
    
    # Enable searching by username or email
    search_fields = ('username',)
    ordering = ('username',)
    # Customize the list view in the admin interface
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Enable searching by username or email
    search_fields = ('username', 'email')