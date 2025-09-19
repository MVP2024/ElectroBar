from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """Доступ только для аутентифицированных активных сотрудников.

    Проверяет, что пользователь аутентифицирован, активен (is_active=True)
    и является сотрудником (is_staff=True).
    """

    message = "Доступ к API разрешён только активным сотрудникам."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
