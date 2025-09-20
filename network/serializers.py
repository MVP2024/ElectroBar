from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers

from contacts.models import ContactInfo
from products.models import Product

from .models import NetworkNode


class ContactInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для ContactInfo"""

    class Meta:
        model = ContactInfo
        fields = [
            "id",
            "email",
            "country",
            "city",
            "street",
            "building_number",
            "structure",
            "block",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date", "node"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор для NetworkNode.

    В соответствии с ТЗ валидация (контроль циклов и глубины иерархии) выполняется на уровне модели
    (NetworkNode.clean()/full_clean()). Сериализатор не дублирует логику проверки глубины/циклов,
    но преобразует ValidationError, брошенный моделью при сохранении, в(serializers.ValidationError),
    чтобы API возвращал корректный HTTP 400 с описанием ошибок.

    Поле debt — только для чтения через API (read_only).
    """

    name = serializers.CharField(label=_("Название"))
    contact = ContactInfoSerializer()
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        allow_null=True,
        required=False,
        help_text=_("PK поставщика (self-relation)"),
    )
    level = serializers.IntegerField(read_only=True, label=_("Уровень"))

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "contact",
            "supplier",
            "debt",
            "created_at",
            "products",
            "level",
        ]
        read_only_fields = ["debt", "created_at", "level"]

    @staticmethod
    def _raise_serializer_validation_error_from_model(exc: DjangoValidationError):
        """Преобразует django.core.exceptions.ValidationError в rest_framework.serializers.ValidationError.

        Если у ValidationError есть attribute message_dict (словарь полей->список сообщений),
        используем его; иначе используем message или messages.
        """
        if hasattr(exc, "message_dict"):
            raise serializers.ValidationError(exc.message_dict)
        # message может быть строкой или списком
        if hasattr(exc, "message") and exc.message:
            raise serializers.ValidationError(exc.message)
        if hasattr(exc, "messages"):
            raise serializers.ValidationError(exc.messages)
        raise serializers.ValidationError(str(exc))

    def create(self, validated_data):
        contact_data = validated_data.pop("contact")
        supplier = validated_data.get("supplier")
        try:
            # Обернул создание contact и node в одну atomic(),
            # чтобы при ошибке валидации модели NetworkNode контакт не оставался хвостом.
            # Также блокируем выбранного supplier (select_for_update), чтобы снизить риск цикла при
            # одновременном создании нескольких клиентов под одним поставщиком.
            with transaction.atomic():
                contact = ContactInfo.objects.create(**contact_data)
                if supplier is not None:
                    # Делаем перезапрос поставщика с блокировкой строки в БД
                    supplier = NetworkNode.objects.select_for_update().get(pk=supplier.pk)
                    # Обновляем validated_data, чтобы в создаваемом объекте использовался заблокированный экземпляр
                    validated_data["supplier"] = supplier
                node = NetworkNode(contact=contact, **validated_data)
                node.save()
                return node
        except DjangoValidationError as exc:
            # Преобразуем модельную ValidationError в форму, понятную DRF
            # и корректно отображаем в ответе API (HTTP 400)
            self._raise_serializer_validation_error_from_model(exc)

    def update(self, instance, validated_data):
        contact_data = validated_data.pop("contact", None)
        # Не обновляем поле debt через API
        validated_data.pop("debt", None)

        try:
            # Оборачиваем обновление contact и самого instance в одну транзакцию atomic(),
            # чтобы при падении создания объекта изменения не остались частично применёнными.
            # Также блокируем supplier (если передан), чтобы снизить риск гонок.
            with transaction.atomic():
                if contact_data:
                    for attr, value in contact_data.items():
                        setattr(instance.contact, attr, value)
                    instance.contact.save()

                supplier = validated_data.get("supplier")
                if supplier is not None:
                    supplier = NetworkNode.objects.select_for_update().get(pk=supplier.pk)
                    validated_data["supplier"] = supplier

                # Обновляем остальные полей на instance и сохраняем с созданием модели
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                return instance
        except DjangoValidationError as exc:
            self._raise_serializer_validation_error_from_model(exc)
