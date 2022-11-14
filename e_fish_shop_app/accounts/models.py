from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models

FIRST_NAME_MAX_LENGTH = 50
LAST_NAME_MAX_LENGTH = 50
USERNAME_NAME_MAX_LENGTH = 50
EMAIL_NAME_MAX_LENGTH = 100
PHONE_NUMBER_NAME_MAX_LENGTH = 50

ADDRESS_1_MAX_LENGTH = 100
ADDRESS_2_MAX_LENGTH = 100
CITY_MAX_LENGTH = 20
COUNTRY_MAX_LENGTH = 20
PROFILE_PICTURE_DIR = 'userprofile'


class MyAccountManager(BaseUserManager):
    """
    Custom manager for users accounts. Overwriting the create_user and create_superuser methods.
    Create normal user and create superuser methods overwritten.
    """

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        if not username:
            raise ValueError('User must have an username.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)


class Account(AbstractBaseUser):
    """
    class Account which customize the user creation.
    Changing the default username login with email login.
    """
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)
    username = models.CharField(max_length=USERNAME_NAME_MAX_LENGTH, unique=True)
    email = models.EmailField(max_length=EMAIL_NAME_MAX_LENGTH, unique=True)
    phone_number = models.CharField(max_length=PHONE_NUMBER_NAME_MAX_LENGTH)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=ADDRESS_1_MAX_LENGTH)
    address_line_2 = models.CharField(blank=True, max_length=ADDRESS_2_MAX_LENGTH)
    profile_picture = models.ImageField(blank=True, upload_to=PROFILE_PICTURE_DIR)
    city = models.CharField(blank=True, max_length=CITY_MAX_LENGTH)
    country = models.CharField(blank=True, max_length=COUNTRY_MAX_LENGTH)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
