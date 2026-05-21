# User Center V3

FastAPI + PostgreSQL + Redis + Docker

Деплой: [https://user-center-mu29.onrender.com](https://user-center-mu29.onrender.com)
Swagger: [https://user-center-mu29.onrender.com/docs](https://user-center-mu29.onrender.com)

## Запуск

docker compose up -d --build

## Тесты

pytest tests/ -v

## Эндпоинты

GET /health - проверка работоспособности
GET /users - список пользователей (пагинация, кэш 60с)
POST /add_user - добавить пользователя
DELETE /clear - очистить БД (требуется админ-пароль)
DELETE /delete_user - удалить пользователя по id (требуется пароль)
GET /stats - статистика (кэш 60с)

## Особенности

- Асинхронный кэш через Redis
- Собственный декоратор @cache
- Интеграционные тесты (15 шт)
- Docker-композ с БД и Redis
- Инвалидация кэша при изменении данных
- Логирование медленных запросов (>0.7с)

## Переменные окружения

DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ADMIN_PASSWORD=...
DEBUG=False

## Статус

Завершён, развёрнут на Render