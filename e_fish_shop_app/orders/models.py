from django.db import models

from e_fish_shop_app.accounts.models import Account
from e_fish_shop_app.store.models import Product, Variation

PAYMENT_ID_MAX_LENGTH = 100
PAYMENT_METHOD_MAX_LENGTH = 100
TOTAL_AMOUNT_PAYED_MAX_LENGTH = 100
STATUS_MAX_LENGTH = 100

ORDER_NUMBER_MAX_LENGTH = 20
FIRST_NAME_MAX_LENGTH = 50
LAST_NAME_MAX_LENGTH = 50
PHONE_MAX_LENGTH = 15
EMAIL_MAX_LENGTH = 50
ADDRESS_LINE_1_MAX_LENGTH = 50
ADDRESS_LINE_2_MAX_LENGTH = 50
COUNTRY_MAX_LENGTH = 50
CITY_MAX_LENGTH = 50
ORDER_NOTES_MAX_LENGTH = 100
ORDER_STATUS_MAX_LENGTH = 10
IP_MAX_LENGTH = 20


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=PAYMENT_ID_MAX_LENGTH)
    payment_method = models.CharField(max_length=PAYMENT_METHOD_MAX_LENGTH)
    total_amount_paid = models.CharField(max_length=TOTAL_AMOUNT_PAYED_MAX_LENGTH)
    status = models.CharField(max_length=STATUS_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=ORDER_NUMBER_MAX_LENGTH)
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)
    phone = models.CharField(max_length=PHONE_MAX_LENGTH)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH)
    address_line_1 = models.CharField(max_length=ADDRESS_LINE_1_MAX_LENGTH)
    address_line_2 = models.CharField(max_length=ADDRESS_LINE_2_MAX_LENGTH, blank=True)
    country = models.CharField(max_length=COUNTRY_MAX_LENGTH)
    city = models.CharField(max_length=CITY_MAX_LENGTH)
    order_note = models.CharField(max_length=ORDER_NOTES_MAX_LENGTH, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=ORDER_STATUS_MAX_LENGTH, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=IP_MAX_LENGTH)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
