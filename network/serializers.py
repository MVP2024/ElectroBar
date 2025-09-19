from rest_framework import serializers

from contacts.models import ContactInfo
from partners.models import Partner
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
    """Сериализатор для NetworkNode. Запрещаем изменение поля debt через API (read_only)."""

    contact = ContactInfoSerializer()
    products = ProductSerializer(many=True, read_only=True)
    partner = serializers.PrimaryKeyRelatedField(queryset=Partner.objects.all(), allow_null=True, required=False)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "contact",
            "supplier",
            "partner",
            "debt",
            "created_at",
            "products",
            "level",
        ]
        read_only_fields = ["debt", "created_at", "level"]

    def create(self, validated_data):
        contact_data = validated_data.pop("contact")
        contact = ContactInfo.objects.create(**contact_data)
        node = NetworkNode.objects.create(contact=contact, **validated_data)
        return node

    def update(self, instance, validated_data):
        contact_data = validated_data.pop("contact", None)
        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()
        # Не обновляем поле debt через API
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)
