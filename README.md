# User Center V3

FastAPI + PostgreSQL + Redis + Docker

## Запуск

docker compose up -d --build

## Тесты

pytest tests/ -v

## Эндпоинты

- GET /health — проверка работоспособности
- GET /users — список пользователей (пагинация, кэш 60с)
- POST /add_user — добавить пользователя
- DELETE /clear — очистить БД (требуется админ-пароль)
- DELETE /delete_user — удалить пользователя по id (требуется пароль)
- GET /stats — статистика (кэш 30с)

## Особенности

- Асинхронный кэш через Redis
- Собственный декоратор @cache
- Интеграционные тесты (15 шт)
- Docker-композ с БД и Redis