from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import NetworkNode
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с NetworkNode.

    Доступ: только активные сотрудники.
    Поле debt — только для чтения через API (запрет на обновление через сериализатор).
    """

    queryset = NetworkNode.objects.all().select_related("contact", "supplier")
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["contact__country"]
    search_fields = ["contact__city"]

    @action(detail=False, methods=["get"])
    def by_country(self, request):
        """Пример action: фильтрация по стране через /by_country/?country=..."""
        country = request.query_params.get("country")
        if not country:
            return Response({"detail": "Параметр country обязателен"}, status=400)
        qs = self.queryset.filter(contact__country=country)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
