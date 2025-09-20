from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """Модель продукта, связанная с конкретным звеном сети."""

    name = models.CharField(max_length=200, verbose_name=_("Название продукта"))
    model = models.CharField(max_length=200, verbose_name=_("Модель"))
    release_date = models.DateField(verbose_name=_("Дата релиза"))
    node = models.ForeignKey(
        "network.NetworkNode",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Звено сети"),
    )

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    def __str__(self):
        return f"{self.name} {self.model}"
