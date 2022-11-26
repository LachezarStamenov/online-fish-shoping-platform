from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse

CATEGORY_NAME_MAX_LENGTH = 40
SLUG_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 255


class Category(models.Model):
    category_name = models.CharField(
        max_length=CATEGORY_NAME_MAX_LENGTH,
        unique=True, validators=(MinLengthValidator(2),)
    )
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH, blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def get_url(self):
        """get the category"""
        return reverse('products by category', args=[self.slug])

    def __str__(self):
        return self.category_name
