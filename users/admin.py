from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(
        label=_("Никнейм"),
        help_text=_("Никнейм для входа. Только буквы, цифры и символы @/./+/-/_."),
    )

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=_("Никнейм"),
        help_text=_("Никнейм для входа. Только буквы, цифры и символы @/./+/-/_."),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = (
        "nickname",
        "email",
        "role",
        "is_employee",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")} ),
        (_("Личные данные"), {"fields": ("first_name", "last_name", "email")} ),
        (_("Бизнес"), {"fields": ("role", "is_employee", "network_node")} ),
        (
            _("Разрешения"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ("last_login", "date_joined")
    raw_id_fields = ("network_node",)

    def nickname(self, obj):
        return obj.get_username()

    nickname.short_description = _("Никнейм")
    nickname.admin_order_field = "username"
