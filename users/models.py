from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("customer", "Customer"),
        ("manager", "Manager"),
        ("other", "Other"),
    ]

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="customer")
    is_employee = models.BooleanField(default=False)

    # Используем строковые ссылки, чтобы избежать циклических импортов
    partner = models.ForeignKey(
        "partners.Partner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )
    network_node = models.ForeignKey(
        "network.NetworkNode",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_username()
