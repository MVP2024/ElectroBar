ElectroBar — учебный Django + DRF проект (сеть продаж электроники)

Кратко
------
Минимум текста — максимум полезного: как запустить проект и работать с API без Swagger/Redoc.

Быстрый запуск (dev)
--------------------
1. Перейти в проект:
   cd D:/Project/courses/ElectroBar
2. Виртуальное окружение (если нужно):
   python -m venv .venv
   .\.venv\Scripts\activate
3. Установить зависимости:
   pip install -r requirements.txt
4. Создать .env по example.env и заполнить значения (SECRET_KEY, DEBUG, DB_...)
5. Применить миграции и создать суперпользователя:
   python manage.py migrate
   python manage.py createsuperuser
6. Запустить сервер:
   python manage.py runserver

Коротко про API
----------------
- Основной маршрут для работы с сетью: /nodes/
  - GET /nodes/ — список
  - POST /nodes/ — создать (требуется аутентификация staff)
  - GET /nodes/{id}/ — деталь
  - PUT/PATCH /nodes/{id}/ — обновление (debt — read_only)
- Доступ разрешён только пользователям с is_active=True и is_staff=True.

Как работать с API без Swagger/Redoc
-----------------------------------
1) Через браузер (DRF Browsable API)
- Откройте http://127.0.0.1:8000/nodes/
- Нажмите "Login" или авторизуйтесь через /admin/ — браузер подставит сессионный cookie и CSRF-токен.
- Удобно для ручного тестирования и создания объектов.

2) curl (рекомендуется Basic Auth для простоты)
- Получить список:
  curl -u admin:password http://127.0.0.1:8000/nodes/
- Получить деталь:
  curl -u admin:password http://127.0.0.1:8000/nodes/3/
- Создать (пример):
  curl -u admin:password -H "Content-Type: application/json" -d '{
    "name":"Магазин №1",
    "contact":{"email":"shop1@example.com","country":"Россия","city":"Москва","street":"Ленина","building_number":"10"},
    "supplier": null
  }' http://127.0.0.1:8000/nodes/

Примечание: SessionAuthentication требует CSRF для POST/PUT/PATCH/DELETE — из терминала работать проще через Basic Auth или JWT (если настроить).

3) Postman / Insomnia
- Используйте Basic Auth (username/password) в Authorization.
- Для Session: надо получить cookie и передавать X-CSRFToken — ненамного удобнее.

Полезные параметры
------------------
- Фильтрация по стране: /nodes/?contact__country=Россия
- Поиск по городу: /nodes/?search=Москва
- Кастомный action: /nodes/by_country/?country=Россия
- supplier задаётся как PK: "supplier": 3

Короткие заметки
-----------------
- Валидация запрещает циклы и ограничивает глубину иерархии (MAX_LEVEL=2).
- Если видите 403 — проверьте, что пользователь аутентифицирован и is_staff=True.
- Для production: DEBUG=False, корректный SECRET_KEY и ALLOWED_HOSTS, включить HTTPS и другие меры безопасности.

Команды
-------
- pip freeze — список пакетов
- python manage.py makemigrations — создать миграции
- python manage.py migrate app_name zero — откат миграций

Если нужно — могу ещё сильнее сократить README или добавить пример curl с CSRF/session. 