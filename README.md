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

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Yana-Denisova/foodgram-project-react.git
```


Пример заполнения .env файла
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=j#@2yv698sb@#x=pq4b!^=4ap1!$b7xgpgv3fbpc5@9017!5jx
```

```
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Авторы проекта

```
- [Денисова Яна](https://t.me/DenisovaYana) - Backend
- [Яндекс.Практикум](https://github.com/yandex-praktikum/foodgram-project-react) - Frontend

```
