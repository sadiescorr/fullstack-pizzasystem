from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime, timedelta, date
import random

from django.forms import ValidationError
#... any other imports

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Topping(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

SIZE = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Supersize', 'Super Size'),
    ]

CRUST = [
        ('Normal', 'Normal'),
        ('Thin', 'Thin'),
        ('Thick', 'Thick'),
        ('Gluten Free', 'Gluten Free'),
    ]

SAUCE = [
        ('Tomato', 'Tomato'),
        ('BBQ', 'BBQ'),
    ]

CHEESE = [
        ('Mozarella', 'Mozarella'),
        ('Vegan', 'Vegan'),
        ('Low Fat', 'Low Fat'),
    ]

TOPPINGS = [
        ('pepperoni', 'Pepperoni'),
        ('chicken', 'Chicken'),
        ('ham', 'Ham'),
        ('pineapple', 'Pineapple'),
        ('peppers', 'Peppers'),
        ('mushrooms', 'Mushrooms'),
        ('onions', 'Onions')
    ]

class Pizza(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False) 
    size = models.CharField(max_length=20, choices=SIZE, default="medium")
    crust = models.CharField(max_length=20, choices=CRUST, default="normal")
    sauce = models.CharField(max_length=20, choices=SAUCE, default="tomato")
    cheese = models.CharField(max_length=20, choices=CHEESE, default="mozarella")
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        toppings_list = ", ".join(t.name for t in self.toppings.all()) or "No Toppings"
        return f"{self.size} {self.crust} crust {self.sauce} base Pizza with {self.cheese} cheese and {toppings_list}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False) 
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=100, blank=False, null=True)
    card_num = models.CharField(max_length=16, blank=False, null=True)
    expiry_date = models.DateField(max_length=5, null=True)
    cvv = models.CharField(max_length=3, blank=False, null=True)
    order_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.expiry_date and self.expiry_date < date.today():
            raise ValidationError("Expiry date must be in the future.")

    def __str__(self):
        return f'Order for {self.pizza}'
