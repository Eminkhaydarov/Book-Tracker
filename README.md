# Book-Tracker
* http://localhost:8000/ - главная страница, здесь отображаюстся последние 4 книги каждой категории
* http://localhost:8000/login - страница входа в учетную запись
* http://localhost:8000/logout - страница выхода
* http://localhost:8000/register - регистрация
* http://localhost:8000/add_book - страница добавления новой книги
* http://localhost:8000/status/favorites - страница со списком всех избраных книг
* http://localhost:8000/status/to_read - страница со списком книг которые пользователь собираеться прочитать
* http://localhost:8000/status/have_read - страница со списком прочитаных книг
* http://localhost:8000/status/reading_now - страница со списком книг, которые пользователь читает сейчас
* http://localhost:8000/book/{slug_book} - информация по конкретной книге
* http://localhost:8000/delete_book/{slug_book} - подтверждение удачения книги удаление книги
* http://localhost:8000/update_book/{slug_book} - изменение книги



# stack
* python 3.11
* Django
* Postgresql

# starting
Создать виртуальное окружение командой
* python -m venv venv

Установить зависимости
* pip install -r requirements.txt

Провести миграции:
* python manage.py makemigrations
* python manage.py migrate

Установить стартовые данные:
* python manage.py loaddata fixtures.initial_data.json

Создать superuser:
* python manage.py createsuperuser

Запустить сервер:
* python manage.py runserver
