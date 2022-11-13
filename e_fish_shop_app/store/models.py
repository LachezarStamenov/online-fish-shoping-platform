from django.db import models
from django.urls import reverse

from e_fish_shop_app.category.models import Category

PRODUCT_MAX_LENGTH = 200
SLUG_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 200
IMAGES_PATH_UPLOAD_TO = 'photos/products'
VARIATION_CATEGORY_MAX_LENGTH = 100
VARIATION_VALUE_MAX_LENGTH = 100


class Product(models.Model):
    product_name = models.CharField(max_length=PRODUCT_MAX_LENGTH, unique=True)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to=IMAGES_PATH_UPLOAD_TO)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        """Function for getting the url path based on the
        view name, category slug and product slug
        """
        return reverse('show product details', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['product_name', 'price']


class VariationManager(models.Manager):
    """
    Class Variation manager which help for managing
    the variation for color and size.
    """
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    """
    Variation model for making dynamic fish size and color choice.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=VARIATION_CATEGORY_MAX_LENGTH, choices=variation_category_choice)
    variation_value = models.CharField(max_length=VARIATION_VALUE_MAX_LENGTH)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.variation_value

