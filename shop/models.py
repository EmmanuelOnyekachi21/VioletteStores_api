from django.db import models
from django.utils.text import slugify

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
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of the Category instance.

        The string is the name of the category, which is useful for display in
        admin interfaces, logs, and debugging.

        Returns:
            str: The name of the category.
        """
        return self.name
    
    class Meta:
        """
        Meta options for the Category Model
        
        Attributes:
            ordering (list): Orders categories by their name.
            indexes (list): Adds an index for the name field to improve
                            query performance.
            verbose_name (str): A human-readable name for the model.
            verbose_name_plural (str): The plural form of the model name.
        """
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
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
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock_quantity = models.IntegerField()
    image = models.ImageField(
        upload_to='products/%Y/%M/%d', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """
        Meta options for the Product model.

        Attributes:
            ordering (list): Orders products by their name.
            indexes (list): Adds indexes for faster querying on specific fields.
        """
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]


    def __str__(self):
        """
        Returns a string representation of the Product instance.

        The string is the name of the product, which helps in displaying the product
        in various views like admin, templates, or logs.

        Returns:
            str: The name of the product.
        """
        return self.name
    
    def save(self, **kwargs):
        """
        Custom save method to ensure the slug field is unique for each product
        If a slug isn't provided, one is generated from the product name.
        """
        if not self.slug:
            base_slug = slugify(self.name)
        else:
            # To ensure the slug is really 'slugged' ;)
            base_slug = slugify(self.slug)
        
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        
        self.slug = slug
        
        super().save(**kwargs)
