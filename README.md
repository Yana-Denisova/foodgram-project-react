# Проект Foodgram - «Продуктовый помощник».


```
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

```
## _RESTful API для проекта Foodgram_

## Технологии проекта 

- При проектировании API мы придерживались принципов REST, 
  что привело к повышению производительности и упрощению архитектуры проекта в целом.
- Foodgram это Django-проект, что позволило подключить библиотеку Django REST Framework,
  которая ускорила разработку REST API. 
- Для обмена данными в API применяется формат JSON.


## Автор проекта Денисова Яна Владимировна 

```
https://github.com/Yana-Denisova/

```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Yana-Denisova/foodgram-project-react.git
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
