from django.db import models
from utils_app.models import BaseModelWithCreatedInfo, Province, City, AppLanguage
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from user_management_app.constants import *
from django.core.validators import MinValueValidator


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        if not phone_number:
            raise ValueError('Users must have an phone_number.')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            phone_number=phone_number,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, username, password):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    # Required Fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # User Defined Fields
    full_name = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=128,  unique=True, null=True, blank=True)
    whatsapp_no = models.CharField(max_length=128,  unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER_CHOICES)
    logo = models.ImageField(upload_to='Logo/User_logo', null=True, blank=True)
    social_platform = models.CharField(max_length=255, choices=SOCIAL_PLATFORM_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=255,  null=True, blank=True)
    document = models.FileField(upload_to='representatives/documents/', null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    fixed_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    per_call_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    services = models.CharField(max_length=255, null=True, blank=True, choices=SERVICE_CHOICES, default='standard')
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES, default='user')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    salary_type = models.CharField(max_length=255, choices=SALARY_TYPPE_CHOICES, default='monthly')
    rep_note = models.TextField(null=True, blank=True)


    # User Defined Fields


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = MyAccountManager()

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    


class Wallet(BaseModelWithCreatedInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username} wallet"
    
class TransactionHistroy(BaseModelWithCreatedInfo):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} to {self.wallet.user.username} Wallet"


class Slot(BaseModelWithCreatedInfo):
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"


class ServicePrice(BaseModelWithCreatedInfo):
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, unique=True)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.service_type} duration {self.duration}Min and its price is ${self.price}"

    

class Booking(BaseModelWithCreatedInfo):
    service_price = models.ForeignKey(ServicePrice, on_delete=models.PROTECT)
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    representative = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'user_type': 'representative'})
    
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.booking_date}"