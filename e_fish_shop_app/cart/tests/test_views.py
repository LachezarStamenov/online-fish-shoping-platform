# from django.contrib.sessions.middleware import SessionMiddleware
# from django.test import TestCase, RequestFactory
# from django.urls import reverse
#
# from e_fish_shop_app.cart.models import Cart
# from e_fish_shop_app.category.models import Category
# from e_fish_shop_app.store.models import Product
#
#
# class CartViewTest(TestCase):
#     """Test the GET view for ViewCart"""
#
#     @classmethod
#     def setUpTestData(cls):
#         category = Category.objects.create(category_name='Saltfishes')
#
#         Product.objects.create(
#             product_name='Catfish',
#             slug='catfish',
#             description='Test description',
#             price=25,
#             is_available=True,
#             stock=3,
#             category=category)
#
#     def setUp(self):
#         self.manual_url = 'cart/'
#         self.reverse_url = reverse('cart')
#         self.factory = RequestFactory()
#         self.request = RequestFactory().get('/')
#         response = self.client.get(self.manual_url)
#         # adding session
#         middleware = SessionMiddleware(response)
#         middleware.process_request(self.request)
#         self.request.session.save()
#         # create basket
#
#         self.product1 = Product.objects.get(product_name='Catfish')
#
#     def test_initialize_cart_clean_session(self):
#         """
#         The cart is initialized with a session that contains no cart.
#         In the end it should have a variable cart which is an empty string.
#         """
#         request = self.request
#         cart = Cart(request.session)
#         self.assertEqual(cart, '')
#
#     def test_initialize_cart_filled_session(self):
#         """
#         The cart is initialized with a session that contains a cart.
#         In the end it should have a variable cart which equal to the cart that
#         is in the initial session.
#         """
#         existing_cart = {
#             '1': self.product1
#         }
#         request = self.request
#         request.session['cart'] = existing_cart
#         cart = Cart(request.session)
#         self.assertEqual(cart, existing_cart)
#
#
#     def test_view_url_exists(self):
#         """Check that the hardcoded page exists"""
#         response = self.client.get(self.manual_url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_reverse_url(self):
#         """Check that the named view page exists"""
#         response = self.client.get(self.reverse_url)
#         self.assertEqual(response.status_code, 200)