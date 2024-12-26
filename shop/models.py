from django.db import models

# Create your models here.
class Category(models.Model):
    """
    Represents a product category in the system.
    Each category can contain multiple products.
    
    Attributes:
        name (str): The name of the category.
        slug (str): A unique URL-friendly identifier for the category.
        description (str): A brief description of the category.
        image (ImageField): An optional image associated with the category.
        created_at (datetime): Timestamp of when the category was created.
        updated_at (datetime): Timestamp of the last update to the category.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of the Category instance.

        The string is the name of the category, which is useful for display in
        admin interfaces, logs, and debugging.

        Returns:
            str: The name of the category.
        """
        return self.name


class Products(models.Model):
    """Represents a product within a specific category.

    Each product is linked to a category and has a:
        - unique name,
        - description,
        - price,
        - and optional image.

    Attributes:
        category (ForeignKey): The category the product belongs to.
        name (str): The name of the product.
        slug (str): A unique URL-friendly identifier for the product.
        description (str): A description of the product.
        price (decimal): The price of the product.
        image (ImageField): An optional image associated with the product.
    """
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        """
        Returns a string representation of the Product instance.

        The string is the name of the product, which helps in displaying the product
        in various views like admin, templates, or logs.

        Returns:
            str: The name of the product.
        """
        return self.name
