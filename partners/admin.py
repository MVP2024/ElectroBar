from django.contrib import admin

from .models import BankAccount, Partner


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 0


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "tax_id", "status", "contact_person_name")
    search_fields = ("name", "tax_id", "contact_person_name")
    list_filter = ("partner_type", "status")
    inlines = [BankAccountInline]
