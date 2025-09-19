from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date", "node")
    list_filter = ("release_date",)
    search_fields = ("name", "model")
