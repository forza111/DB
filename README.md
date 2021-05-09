# DJANGO BANK
Приложение DJANGO BANK позволяет администратору создавать пользователей со счетами и кредитами. На данный момент функционал не доработан, 
для администратора открыты следующиие возможности: добавлять пользователей и всю контактную информацию; добавлять типы счетов/процентную ставку для кредита и т.д.
для пользователей: авторизовывваться, смотреть курс валют, смотреть графк платежей по кредиту

# Как пользоваться?
## Установите и настройте виртуальное окружение
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

## Установите мииграции
python manage.py migrate

## Сделайте импорт БД
python manage.py loaddata db.json

## Запустите сервер
python manage.py runserver

## Откройте http://127.0.0.1:8000/ и войдите используя следующие данные:
Логин Никита
Пароль nikitadjango

## Для админиистриирования используйте следующиие данные:
Логин admin
Пароль admin
