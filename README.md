# Книга рецептов FoodGRAM
![Bage](https://github.com/kirefim/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

[ссылка](https://ellrik92.ddns.net/api/docs/) на документацию

https://ellrik92.ddns.net/ проект на сервере

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
Список доступных эндпоинтов к API доступен по адресу  http://localhost:8000/api/

Для доступа к админ-панели необходимо создать суперюзера:
```
docker-compose exec web python manage.py createsuperuser
```
Админ-панель доступна по адресу http://localhost:8000/admin/

**Для подключения SPA к API (неообходим установленный Node.js)**

В новом окне терминала переходим в директорию frontend/ и устанавливаем зависимости:
```
npm install --legacy-peer-deps
```
Запускаем SPA фронтенд:
```
npm run start
```
Полностью проект доступен по адресу http://localhost:3000

### Стек технологий
| | |
| ---------------- | - |
| Фронтенд | React ([Яндекс Практикум](https://practicum.yandex.ru/)) |
| Бэкенд | Python 3.7, Django 4.1.4, Django REST Framework 3.14.0, Postgres 15.0 |
| Инфрастуктура| Docker, Github Actions, nginx, gunicorn |

### Автор
Ефимкин Кирилл
