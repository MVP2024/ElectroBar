from django.contrib import admin

from .models import ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "country",
        "city",
        "street",
        "building_number",
        "structure",
        "block",
    )
    search_fields = ("email", "city", "country")
