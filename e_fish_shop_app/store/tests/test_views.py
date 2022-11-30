from django.test import TestCase

from django.urls import reverse

from e_fish_shop_app.store.models import ReviewRating
from e_fish_shop_app.store.tests.utils import create_products, create_user

PRODUCTS_COUNT = 5


class ProductListViewTest(TestCase):
    """Store view tests"""
    def setUp(self):
        create_products(PRODUCTS_COUNT)
        self.manual_url = '/store/'
        self.reverse_url = reverse('store')

    def test_view_url_exists(self):
        response = self.client.get(self.manual_url)
        self.assertEqual(response.status_code, 200)

    def test_view_reverse_url(self):
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_view_template_used_is_correct(self):
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_view_product_count_return_correct_value(self):
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.context['products_count'], PRODUCTS_COUNT)

    def test_view_context_contain_correct_products(self):
        response = self.client.get(self.reverse_url)
        self.assertEqual(len(response.context['products']), PRODUCTS_COUNT)


class ProductDetailView(TestCase):
    """Product detail view tests"""
    def setUp(self):
        self.product = create_products(1)
        category_slug = 'test'
        product_slug = ''.join(pr.slug for pr in self.product)
        self.manual_url = '/store/category/' + category_slug + '/' + product_slug + '/'
        self.reverse_url = reverse('show product details', kwargs={
            'category_slug': category_slug, 'product_slug': product_slug})
        user = create_user()
        self.reviews = ReviewRating.objects.create(product=self.product[0], user=user, rating =6, status=True)

    def test_view_url_exists_return_200(self):
        response = self.client.get(self.manual_url)
        self.assertEqual(response.status_code, 200)

    def test_view_reverse_url_return_200(self):
        response = self.client.get(self.reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_view_invalid_product_id_return_404(self):
        response = self.client.get('/products/asdf/')
        self.assertEqual(response.status_code, 404)

    def test_view_template_is_correct(self):
        response = self.client.get(self.reverse_url)
        self.assertTemplateUsed(response, 'store/product_details.html')

    def test_view_check_if_context_fields_exists(self):
        response = self.client.get(self.reverse_url)
        self.assertTrue('product' in response.context)
        self.assertTrue('reviews' in response.context)
        self.assertTrue('is_in_cart' in response.context)
        self.assertTrue('ordered_product' in response.context)
        self.assertTrue('product_gallery' in response.context)

    def test_reviews_return_correct_values(self):
        count_reviews = self.product[0].count_review()
        average_reviews = self.product[0].average_review()
        self.assertEqual(count_reviews, 1)
        self.assertEqual(average_reviews, 6)
