# Книга рецептов FoodGRAM

### Описание

Проект FoodGRAM представляет собой фуллстек онлайн-сервис для публикации авторами рецептов (SPA фронтенд на React, API бэкенд на Django + Django REST Framework).
Взаимодействие фронтенда и бэкенда реализовано с использованием контейнерезации Docker.

**Функционал приложения поддерживает (для авторизованных пользователей):**

- публикацию рецепта, с указанием необходимых ингредиетов, их количества, 
- добавление тэгов к публикуемому рецепту, 
- возможность подписываться на публикации понравившихся авторов,
- добавление понравившихся рецептов в список «Избранное»,
- формирование сводного списка продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Аутентификация реализована с использованием стандартных Auth токенов.
Проект api_yamfb реализован в контейнерах docker, автоматизация с деплоем на боевой сервер, CI с использованием Github Actions.

### Как запустить проект

Клонировать репозиторий:
```
git clone git@github.com:kirefim/foodgram-project-react.git
```

**Для локального запуска только API**

Перейдите в директорию api_foodgram:
```
cd foodgram-project-react/backend/api_foodgram
```
Cоздать и активировать виртуальное окружение, обновить pip:
```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
```
Создайте файл виртуального окружения **.env**
```
touch .env
```
Пример заполнения файла:
```
#main settings
SECRET_KEY=secret_key
DEBUG=True
PRODUCTION=False
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Собрать статику, накатить миграции:
```
python manage.py collectstatic --no-input
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```

**Для локального запуска проекта целиком (необходим установленный Docker):**

Перейдите в директорию infra:
```
cd foodgram-project-react/infra
```
Создайте файл виртуального окружения **.env**
```
touch .env
```
Пример заполнения файла:
```
#database
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=1488 # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
#main settings
SECRET_KEY=secret_key
DEBUG=True
PRODUCTION=False
```
Создайте образы и соберите контейнеры:
```
docker-compose up -d --build
```
Список доступных эндпоинтов к API доступен по адресу  http://localhost/api/

Локально проект доступен по адресу http://localhost/

Для доступа к админ-панели необходимо создать суперюзера:
```
docker-compose exec web python manage.py createsuperuser
```
Админ-панель доступна по адресу http://localhost/admin/

### Стек технологий
| | |
| ---------------- | - |
| Фронтенд | React ([Яндекс Практикум](https://practicum.yandex.ru/)) |
| Бэкенд | Python 3.7, Django 4.1.4, Django REST Framework 3.14.0, Postgres 15.0 |
| Инфрастуктура| Docker, Github Actions, nginx, gunicorn |

### Автор
Ефимкин Кирилл
