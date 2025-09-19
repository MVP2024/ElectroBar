from django.db import models


class Product(models.Model):
    """Модель продукта, связанная с конкретным звеном сети."""

    name = models.CharField(max_length=200, verbose_name="Название продукта")
    model = models.CharField(max_length=200, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата релиза")
    node = models.ForeignKey(
        "network.NetworkNode",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Звено сети",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} {self.model}"
