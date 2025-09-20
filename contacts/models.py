from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactInfo(models.Model):
    """Контакты для звена сети.

    Хранит email и адрес
    """

    email = models.EmailField(
        verbose_name=_("Email"), help_text=_("Контактный адрес электронной почты")
    )
    country = models.CharField(max_length=100, verbose_name=_("Страна"), db_index=True)
    city = models.CharField(max_length=100, verbose_name=_("Город"), db_index=True)
    street = models.CharField(max_length=200, verbose_name=_("Улица"))
    building_number = models.CharField(max_length=50, verbose_name=_("Номер дома"))
    structure = models.CharField(max_length=50, verbose_name=_("Строение"), blank=True)
    block = models.CharField(max_length=50, verbose_name=_("Корпус"), blank=True)

    class Meta:
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")

    def __str__(self):
        parts = [self.city, f"{self.street} {self.building_number}"]
        if self.structure:
            parts.append(f"стр. {self.structure}")
        if self.block:
            parts.append(f"корп. {self.block}")
        return ", ".join(parts) + f" ({self.email})"
