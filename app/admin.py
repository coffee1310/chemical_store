from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username",'created_at')
    list_display_links = ("username",)
    search_fields = ("username",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","product_name","cat")
    list_display_links = ("product_name",)
    search_fields = ("product_name",)
    prepopulated_fields = {"product_slug":("product_name",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","cat")
    list_display_links = ("cat",)
    search_fields = ("cat",)
    prepopulated_fields = {"cat_slug":("cat",)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user","date_ordered","total_amount")
    list_display_links = ("user","date_ordered")
    search_fields = ("user","date_ordered")

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id","order","product")
    list_display_links = ("order","product")
    search_fields = ("order","product")

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)