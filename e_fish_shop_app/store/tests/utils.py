from django.contrib.auth import get_user_model

from e_fish_shop_app.category.models import Category
from e_fish_shop_app.store.models import Product


def create_products(count):
    category = Category.objects.create(category_name='Test', slug='test')
    products = []
    for i in range(count):
        product_name = f'Catfish{i}'
        slug = f'catfish{i}'
        description = f'Test description{i}'
        price = (20 + i)
        is_available = True
        stock = 3
        images = 'e_fish_shop_app/store/tests/image.jpg'

        product_details = {
            'product_name': product_name,
            'slug': slug,
            'description': description,
            'price': price,
            'images': images,
            'is_available': is_available,
            'stock': stock,
            'category': category,
        }
        products.append(Product.objects.create(**product_details))
    return products


def create_user():
    user_details = {
        'email': 'test_user@test.com',
        'username': 'test_user',
        'first_name': 'Test',
        'last_name': 'User',
        'password': '1214_tough_password1!',
    }

    return get_user_model().objects.create_user(**user_details)
