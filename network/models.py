from django.db import models

from contacts.models import ContactInfo


class NetworkNode(models.Model):
    """Модель звена в иерархии сети."""

    name = models.CharField(max_length=200, verbose_name="Название")
    contact = models.OneToOneField(
        ContactInfo, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Задолженность"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self):
        return self.name

    @property
    def level(self) -> int:
        """Вычисляет уровень звена в иерархии.

        Возвращает 0 для завода (нет поставщика), 1 для прямого клиента завода и 2 для клиента уровня 1.
        Если цепочка длиннее, будет возвращён фактический уровень (count).
        """
        level = 0
        node = self
        while node.supplier is not None:
            level += 1
            node = node.supplier
            if level > 10:
                # Защита от бесконечной рекурсии в случае циклов
                break
        return level
