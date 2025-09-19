from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Admin для NetworkNode: показывает ссылку на поставщика, фильтр по городу и action для обнуления долга."""

    list_display = ("name", "supplier_link", "debt", "created_at", "level")
    list_filter = ("contact__city",)
    search_fields = ("name", "contact__city")
    actions = ("clear_debt_action",)

    def supplier_link(self, obj):
        """Возвращает HTML-ссылку на страницу поставщика в админке или прочерк, если поставщика нет."""
        if not obj.supplier:
            return "-"
        url = reverse("admin:network_networknode_change", args=(obj.supplier.pk,))
        return format_html('<a href="{}">{}</a>', url, obj.supplier)

    supplier_link.short_description = _("Поставщик")
    supplier_link.admin_order_field = "supplier"

    def clear_debt_action(self, request, queryset):
        """Admin action: обнуляет задолженность у выбранных объектов."""
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность обнулена у {updated} объектов")

    clear_debt_action.short_description = "Обнулить задолженность у выбранных"
