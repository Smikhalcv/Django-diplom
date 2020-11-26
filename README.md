## Дипломный проект

### Интернер магазин

Для запуска приложение необходимо выполнить следующие шаги:
* Установить Git `$ sudo apt-get git`
* Клонировать репозиторий `$ git clone -URL проекта на GitHub`
* Перейти в образовавшийся каталог `$ cd diplom_django`
* Установить Python используя команду в терминале
`$ sudo apt-get install python`
* Установить модуль для виртуального окружения на Python 
`$ pip install virtualenv`
* Создать виртуальное окружение `$ python3 -m venv env`
* Активировать виртуальное окружение `$ source env/bin/activate`
* Установить зависимости и необходимые компоненты `$ pip install -r requirements.txt`
* Создать в корне проекта файл `.env` и указать в нём `SECRET_KEY = 'какой-то ключ'`
* Выполнить миграции для проекта `$ python3 manage.py migrate`
* Перенести данные базы данных `$ python3 manage.py loaddata fixtures.json`
* Выполнить запуск проекта `$ python3 manage.py runserver`

### *Проект готов к использованию!*
