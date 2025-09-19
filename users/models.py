from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    ROLE_CHOICES = [
        ("employee", _("Сотрудник")),
        ("customer", _("Клиент")),
        ("manager", _("Менеджер")),
        ("other", _("Другое")),
    ]

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="customer",
                            verbose_name=_("Роль пользователя"),
                            help_text=_("Выберите роль пользователя: влияет на доступы в системе."))
    is_employee = models.BooleanField(default=False, verbose_name=_("Сотрудник"),
                                      help_text=_("Отмечается для сотрудников компании (дополнительные права)."))

    # Используем строковые ссылки, чтобы избежать циклических импортов
    partner = models.ForeignKey(
        "partners.Partner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name=_("Партнёр"),
        help_text=_("Связать пользователя с партнёром (если применимо).")
    )
    network_node = models.ForeignKey(
        "network.NetworkNode",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name=_("Звено сети"),
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_username()
