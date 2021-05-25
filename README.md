# Приложение «Продуктовый помощник» 
## Функционал:
- Позволяет публиковать рецепты
- Добавлять рецепты в избранное
- Подписываться на публикации других авторов
- Сервис "Список покупок", позволяет создавать список продуктов, который потом можно скачать
- Интерфейс администратора

## Подготовка рабочей среды
Перейдите в свою рабочую директорию и выполните следующие команды:
```
git clone https://github.com/avcherezov/foodgram-project
cd foodgram-project
```
Создайте в корне проекта файл .env со следующими данными:
```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY = uja*@@0a6y0j1lb*r5c9io=_1s3c$5%7qo(&oil1%r5r#zz-6f
```
Выполните команду:
```
docker-compose up --build -d
```
Выполните миграции:
```
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Заполните базу данных:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Запустите сервер разработки:
```
docker-compose exec web python manage.py runserver
```

## Стэк
Django, Gunicorn, Nginx, PostgreSQL, Docker, Яндекс.Облако
