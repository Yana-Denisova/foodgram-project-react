# Foodgram - Продуктовый помощник.

## Содержание
- [Описание проекта](#описание-проекта)
- [Технологии проекта](#технологии-проекта)
- [Как запустить проект](#как-запустить-проект)
- [Авторы проекта](#авторы-проекта)


## Описание проекта
```
Социальная сеть для публикации кулинарных рецептов, с возможностью подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.
При проектировании API я придерживалась принципов REST, что привело к повышению производительности и упрощению архитектуры проекта в целом.
Foodgram это Django-проект, что позволило подключить библиотеку Django REST Framework, которая ускорила разработку REST API. 
Для обмена данными в API применяется формат JSON.

```

## Технологии проекта 
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Yandex.Cloud](https://cloud.yandex.ru/)


## Как запустить проект:

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/Yana-Denisova/foodgram-project-react.git
SSH: git clone git@github.com:Yana-Denisova/foodgram-project-react.git
```
Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
Linux: source venv/bin/activate
Windows: source venv/Scripts/activate
```
И установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Проект использует базу данных PostgreSQL.  
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл ".env" с переменными окружения в папке "./infra/".

Шаблон для заполнения файла ".env":
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='Здесь указать секретный ключ'
ALLOWED_HOSTS='Здесь указать имя или IP хоста' (Для локального запуска - 127.0.0.1)
```


Соберите контейнеры из папки `infra`:
```py
docker-compose up -d
```
- В контейнере **backend**:
    - выполните миграции;
    - установите **superuser**;
    - заполните БД исходными данными:

```py
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py runscript load_ing_data
```


## Авторы проекта

- [Денисова Яна](https://t.me/DenisovaYana) - Backend
- [Яндекс.Практикум](https://github.com/yandex-praktikum/foodgram-project-react) - Frontend

