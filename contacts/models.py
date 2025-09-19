from django.db import models


class ContactInfo(models.Model):
    """Контакты для звена сети.

    Хранит email и адрес
    """

    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна", db_index=True)
    city = models.CharField(max_length=100, verbose_name="Город", db_index=True)
    street = models.CharField(max_length=200, verbose_name="Улица")
    building_number = models.CharField(max_length=50, verbose_name="Номер дома")
    structure = models.CharField(max_length=50, verbose_name="Строение", blank=True)
    block = models.CharField(max_length=50, verbose_name="Корпус", blank=True)

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        parts = [self.city, f"{self.street} {self.building_number}"]
        if self.structure:
            parts.append(f"стр. {self.structure}")
        if self.block:
            parts.append(f"корп. {self.block}")
        return ", ".join(parts) + f" ({self.email})"
