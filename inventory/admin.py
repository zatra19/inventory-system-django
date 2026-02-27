from django.contrib import admin
from .models import Category, Supplier, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'category', 'supplier', 'stock', 'price')
    search_fields = ('name', 'code')
    list_filter = ('category', 'supplier')