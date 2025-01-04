# from django.db import models
# from django.contrib import redirects
# from django.http import *
# from typing import Any
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.core.exceptions import ValidationError
# from django.db.models import UniqueConstraint
# from django.db.models.functions import Lower



# # Create your models here.

# # Custom User Manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Please provide a valid Email!!")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)


# # Custom User Model
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=200, unique=True)
#     email = models.EmailField(max_length=200, unique=True)
#     user_address = models.CharField(max_length=200)
#     user_phone = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
    
#     objects = CustomUserManager()
    
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
        
#     def get_full_name(self):
#         return self.username  
    
    
    
# class Category(models.Model):
#     category_name= models.CharField(max_length=200)
#     def __str__(self):
#         return self.category_name

    
      
    
# class Food_items(models.Model):
#     itemname = models.CharField(max_length=200)
#     food_image = models.ImageField(upload_to="product",null=True, blank=True)
#     itemprice = models.IntegerField()
#     discount = models.IntegerField()
#     food_description=models.TextField(max_length=1000)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     item_quantity = models.IntegerField()
    
#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 Lower('itemname'),
#                 name='unique_itemname_case_insensitive'
#             )
#         ]

    
#     def clean(self):
#         if self.itemprice <= 0:
#             raise ValidationError({'itemprice': 'Item price must be a positive number.'})
#         if self.item_quantity <= 0:
#             raise ValidationError({'item_quantity': 'Item quantity must be a positive number.'})

#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return self.itemname
    
#     def clean(self):
#         if self.itemprice <= 0:
#             raise ValidationError({'itemprice': 'Item price must be a positive number.'})
#         if self.item_quantity <= 0:
#             raise ValidationError({'item_quantity': 'Item quantity must be a positive number.'})

#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)

#     # @property
#     # def food_imageURL(self):
#     #     try:
#     #         url = self.food_image.url
#     #     except:
#     #         url = ''
#     #     return url
    

    
    

    
# #cart
# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     item = models.ForeignKey(Food_items, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')

#     def __str__(self):
#         return f"{self.item.itemname} ({self.quantity})"    
    
    
# #Order


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('PLACED', 'Order Placed'),
#         ('APPROVED', 'Order Approved'),
#         ('SHIPPED', 'Order Shipped'),
#         ('DELIVERED', 'Order Delivered'),
#         ('CANCELLED', 'Order Cancelled')
#     )
    
#     PAYMENT_CHOICES=(
#         ('COD', 'Cash On Delivery'),
#         ('ONLINE', 'Online Payment'),
        
#     )
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(CartItem)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     receiver_name = models.CharField(max_length=200)
#     receiver_phone = models.CharField(max_length=15)
#     receiver_address = models.CharField(max_length=200)
    
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Order #{self.id} - {self.user.username}"

# class OrderDetail(models.Model):
#     order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
#     # item_name = models.CharField(max_length=100)
#     item = models.ForeignKey(Food_items, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.item.itemname} - {self.quantity} pcs"

# # @receiver(post_save, sender=Order)
# # def create_order_details(sender, instance, created, **kwargs):
# #     if created:
# #         for item in instance.items.all():
# #             OrderDetail.objects.create(order=instance, item_name=item.item.itemname)

# # Signal to update product quantity when order is approved
# @receiver(post_save, sender=Order)
# def update_item_quantity(sender, instance, **kwargs):
#     if instance.status == 'APPROVED':
#         order_details = OrderDetail.objects.filter(order=instance)
#         for detail in order_details:
#             item = detail.item
#             item.item_quantity -= detail.quantity
#             item.save()



from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please provide a valid Email!!")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    user_address = models.CharField(max_length=200)
    user_phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        return self.username  
    
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

    
class Food_items(models.Model):
    itemname = models.CharField(max_length=200)
    food_image = models.ImageField(upload_to="product", null=True, blank=True)
    itemprice = models.IntegerField()
    discount = models.PositiveIntegerField()
    food_description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_quantity = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('itemname'),
                name='unique_itemname_case_insensitive'
            )
        ]

    def __str__(self):
        return self.itemname
    
    def clean(self):
        if self.itemprice <= 0:
            raise ValidationError({'itemprice': 'Item price must be a positive number.'})
        if self.item_quantity <= 0:
            raise ValidationError({'item_quantity': 'Item quantity must be a positive number.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    
    
# Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Food_items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')

    def __str__(self):
        return f"{self.item.itemname} ({self.quantity})"    
    
    
# Order
class Order(models.Model):
    STATUS_CHOICES = (
        ('PLACED', 'Order Placed'),
        ('APPROVED', 'Order Approved'),
        ('SHIPPED', 'Order Shipped'),
        ('DELIVERED', 'Order Delivered'),
        ('CANCELLED', 'Order Cancelled')
    )
    
    PAYMENT_CHOICES = (
        ('COD', 'Cash On Delivery'),
        ('ONLINE', 'Online Payment'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_name = models.CharField(max_length=200)
    receiver_phone = models.CharField(max_length=15)
    receiver_address = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    item = models.ForeignKey(Food_items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.itemname} - {self.quantity} pcs"

# Signal to update product quantity when order is approved
@receiver(post_save, sender=Order)
def update_item_quantity(sender, instance, **kwargs):
    if instance.status == 'APPROVED':
        order_details = OrderDetail.objects.filter(order=instance)
        for detail in order_details:
            item = detail.item
            item.item_quantity -= detail.quantity
            item.save()
