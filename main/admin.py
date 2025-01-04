# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# # Register your models here.
# from django.contrib import admin
# from .models import*


# # Register your models here.
# class UserAdmin(BaseUserAdmin):
#     list_display = ('email', 'username', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('username', 'user_address', 'user_phone')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)


# admin.site.register(User)

# # admin.site.register(Order)

# admin.site.register(Category)

# admin.site.register(Food_items)

# class Food_itemsAdmin(admin.ModelAdmin):
#       list_filter = ('food_category',)
      

# admin.site.register(OrderDetail)

# class OrderDetailInline(admin.TabularInline):
#     model=OrderDetail
#     readonly_fields = ('item_name',)
#     can_delete = False
#     extra = 0
    
# class OrderAdmin(admin.TabularInline):
#     list_display=('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
#     list_filter = ('status', 'created_at', 'updated_at')
#     search_fields = ('user__username', 'user__email')
#     inlines = [OrderDetailInline]

# admin.site.register(Order, OrderAdmin)

from django.contrib import admin
from .models import User, Category, Food_items, Cart, CartItem, Order, OrderDetail

# Register your models here.


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ('item', 'quantity', 'price')
    extra = 0
    fields = ('item', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'payment_method','created_at', 'updated_at', 'receiver_name', 'receiver_phone', 'receiver_address')
    # list_filter = ('status', 'created_at', 'updated_at')
    # search_fields = ('user__username', 'user__email')
    inlines = [OrderDetailInline]
    fields = ('user', 'status', 'total_price')
    readonly_fields = ('created_at', 'updated_at')
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('details__item')  # Optimize for better performance
        return queryset


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Food_items)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderDetail)
admin.site.register(Order, OrderAdmin)
