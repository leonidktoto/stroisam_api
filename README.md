# Интернет-магазин стройматериалов API

## Описание
Этот проект представляет собой API для интернет-магазина стройматериалов, разработанный с использованием FastAPI. API предоставляет функциональность для управления категориями товаров, продуктами, пользователями, корзиной и заказами.

## Стек технологий
- **Язык программирования**: Python 3.12
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy
- **Миграции**: Alembic
- **Хранение изображений**: S3 (Яндекс Cloud)
- **Кеширование**: Redis
- **Фоновые задачи**: Celery
- **Трекер ошибок**: Hawk (open-source)
- **Рассылка SMS**: SMS Aero
- **Запуск через контейнеризацию**: Docker Compose

## Установка
### Требования:
- Python 3.12
- Docker и Docker Compose

### Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Запуск с помощью Docker Compose:
```bash
docker-compose up --build
```

## Документация API
После запуска сервер доступен по адресу:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Эндпоинты API

### Категории товаров
- `GET /categories/main` - Получить главные категории
- `GET /categories/sub/{parent_id}` - Получить подкатегории

### Товары
- `GET /products/category/{category_id}` - Получить товары по категории
- `GET /products/id/{id}` - Получить товар по ID
- `POST /products/filter` - Фильтрация товаров
- `GET /products/filters/options` - Получить параметры фильтрации
- `GET /products/search` - Поиск товаров
- `GET /products/autocomplete` - Автозаполнение поиска

### Аутентификация и пользователи

В проекте реализована аутентификация и авторизация на основе **JWT** (access и refresh токены), которые хранятся в **cookies**.

- `POST /users/register` - Регистрация пользователя
- `POST /users/sms_verification` - Верификация через SMS
- `POST /users/login/` - Вход в систему
- `POST /users/logout` - Выход из системы
- `POST /users/refresh/` - Обновление(получение) access JWT-токена на основании refresh JWT-токена
- `GET /users/me/` - Получить информацию о пользователе

### Корзина
- `GET /users/cart/` - Получить содержимое корзины
- `POST /users/cart/items` - Добавить товар в корзину
- `DELETE /users/cart/items` - Очистить корзину
- `PATCH /users/cart/items` - Частичное обновление товара в корзине
- `DELETE /users/cart/items/{id}` - Удалить товар из корзины

### Заказы
- `GET /users/orders` - Получить список заказов пользователя
- `POST /users/orders/checkout` - Оформить заказ
- `GET /users/orders/{order_id}` - Получить детали заказа
- `POST /users/orders/{order_id}/cancel` - Отменить заказ
- `POST /users/orders/{order_id}/reorder` - Повторить заказ