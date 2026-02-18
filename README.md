# Test Assignment for Junior Backend Developer

### О задании
В реальном проекте мы работаем с Direct сообщениями, но для тестового выбрали API постов и комментариев. Это самый простой способ проверить навыки интеграции с внешними сервисами, не заставляя вас тратить лишнее время на сложную логику доступов. Нам важно увидеть, как вы проектируете архитектуру и работаете с данными.


## Задача
Разработать сервис на **Django + DRF**, который синхронизирует контент из Instagram в локальную базу данных и позволяет управлять комментариями через API.

## Стек
* **Python 3.10+**, **Django**, **DRF**.
* **PostgreSQL**.
* **Docker** & **Docker Compose**.


## Функциональность

- **POST /api/sync/** — загружает все медиа-объекты пользователя из Instagram (с обработкой пагинации) и сохраняет/обновляет их в базе (upsert).
- **GET /api/posts/** — возвращает список сохранённых постов с пагинацией (CursorPagination).
- **POST /api/posts/{id}/comment/** — отправляет комментарий к посту в Instagram и сохраняет его локально.

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone git@github.com:temm-dev/Test-task-Junior-Backend.git
cd Test-task-Junior-Backend
```

### 2. Создать файл .env

```bash
cp .env.example .env
```

#### Заполнить своими данными
```.env
INSTAGRAM_ACCESS_TOKEN=ваш_токен
INSTAGRAM_USER_ID=ваш_user_id
DB_NAME=instagram_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```


### 3.  Запустить контейнеры

```bash
docker-compose up --build
```

При первом запуске будут скачаны образы и созданы контейнеры. <br>
После успешного старта сервер будет доступен по адресу http://localhost:8000

### 4. Применить миграции

```bash
docker-compose exec web python manage.py migrate
```

### 5. (Опционально) Создать суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

Админка доступна по http://localhost:8000/admin

## Примеры запросов API

### Синхронизация постов

```bash
curl -X POST http://localhost:8000/api/sync/
```


### Список постов
```bash
curl -X GET http://localhost:8000/api/posts/
```

Ответ с пагинацией:

```json
{
  "next": "http://localhost:8000/api/posts/?cursor=...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "instagram_id": "17912345678901234",
      "caption": "Мой пост",
      "media_type": "IMAGE",
      "media_url": "https://...",
      "permalink": "https://www.instagram.com/p/...",
      "timestamp": "2026-02-18T09:29:48Z",
      "updated_at": "2026-02-18T09:32:42.277341Z"
    }
  ]
}
```

### Отправка коментария

```bash
curl -X POST http://localhost:8000/api/posts/1/comment/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет из API!"}'
```

Успешный ответ

```json
{
  "id": 5,
  "instagram_id": "17895634567890123",
  "post": 1,
  "text": "Привет из API!",
  "timestamp": "2026-02-18T13:45:12Z",
  "username": "",
  "created_at": "2026-02-18T13:45:12.123456Z"
}
```

## Тестирование

### Запуск тестов

```bash
docker-compose exec web python manage.py test
```

<br>

P.s. - Изначально не был знаком с Django, но мне было интересно выполнить задание. Использовал deepseek для базовой структуры и объяснения концепций. Разобрал каждый кусок кода, адаптировал решение под требования и полностью понимаю(наверное), как работает каждая часть проекта. Желаю пройти тестовое задание, показать способность к обучению