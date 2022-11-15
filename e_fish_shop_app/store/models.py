from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse

from e_fish_shop_app.accounts.models import Account
from e_fish_shop_app.category.models import Category

PRODUCT_MAX_LENGTH = 200
SLUG_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 200
IMAGES_PATH_UPLOAD_TO = 'photos/products'
VARIATION_CATEGORY_MAX_LENGTH = 100
VARIATION_VALUE_MAX_LENGTH = 100

SUBJECT_MAX_LENGTH = 100
REVIEW_MAX_LENGTH = 500
IP_MAX_LENGTH = 20

PRODUCT_IMAGE_MAX_LENGTH = 255
PRODUCT_IMAGE_UPLOAD_DIR = 'store/products'


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

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

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


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=SUBJECT_MAX_LENGTH, blank=True)
    review = models.TextField(max_length=REVIEW_MAX_LENGTH, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=IP_MAX_LENGTH, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    """Product Gallery model for creating unlimited fish images"""

    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=PRODUCT_IMAGE_UPLOAD_DIR, max_length=PRODUCT_IMAGE_MAX_LENGTH)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'
