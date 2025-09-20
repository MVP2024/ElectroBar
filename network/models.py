from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from contacts.models import ContactInfo


class NetworkNode(models.Model):
    """Модель звена в иерархии сети."""

    MAX_LEVEL = 2  # разрешены уровни 0 (завод), 1 (розничная сеть), 2 (ИП)

    name = models.CharField(
        max_length=200, verbose_name=_("Название"), help_text=_("Имя звена в сети")
    )
    contact = models.OneToOneField(
        ContactInfo, on_delete=models.CASCADE, verbose_name=_("Контакты")
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name=_("Поставщик"),
        help_text=_("Поставщик в иерархии сети (self-relation)"),
    )
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Задолженность"),
        help_text=_("Текущая задолженность"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Время создания")
    )

    class Meta:
        verbose_name = _("Звено сети")
        verbose_name_plural = _("Звенья сети")

    def __str__(self):
        return self.name

    @property
    def level(self) -> int:
        """Вычисляет уровень звена в иерархии.

        Возвращает 0 для завода (нет поставщика), 1 для прямого клиента завода и 2 для клиента уровня 1.
        """
        level = 0
        node = self
        visited = set()
        while node.supplier is not None:
            # защита от бесконечной рекурсии в случае циклов
            if node.pk in visited:
                break
            visited.add(node.pk)
            level += 1
            node = node.supplier
            if level > 100:
                # дополнительная защита
                break
        return level

    def clean(self):
        """Валидация: предотвращаем циклы и ограничиваем глубину до MAX_LEVEL."""
        # supplier не может быть самим объектом
        if (
            self.pk is not None
            and self.supplier is not None
            and self.supplier.pk == self.pk
        ):
            raise ValidationError({"supplier": "Поставщиком не может быть сам объект."})

        # проверка циклов: подняться по цепочке поставщиков и убедиться, что текущий объект не встречается
        node = self.supplier
        while node is not None:
            if node.pk == self.pk:
                raise ValidationError(
                    {"supplier": "Назначение этого поставщика создаёт цикл в иерархии."}
                )
            node = node.supplier

        # проверка глубины: уровень = supplier.level + 1
        if self.supplier is not None:
            if self.supplier.level + 1 > self.MAX_LEVEL:
                raise ValidationError(
                    {
                        "supplier": f"Максимальный допустимый уровень — {self.MAX_LEVEL} (0..{self.MAX_LEVEL})."
                    }
                )

    def save(self, *args, **kwargs):
        # Вызываем full_clean, чтобы применить модельную валидацию при сохранении из кода/админки
        self.full_clean()
        super().save(*args, **kwargs)
