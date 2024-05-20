# Тестовое задание REST API для групповых денежных сборов

## О проекте

Этот проект представляет собой веб-сервис на базе Django, который предоставляет CRUD REST API для групповых денежных сборов. Пользователи могут создавать сборы, приглашать других пользователей к участию, делать пожертвования и просматривать информацию о текущем состоянии сбора.


## Технологии

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoRESTFramework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://swagger.io/)

## Начало работы

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере для разработки и тестирования.

### Предварительные требования

Убедитесь, что у вас установлены Docker и Docker Compose. Это можно сделать, следуя официальной документации Docker: [установка Docker](https://docs.docker.com/get-docker/) и [установка Docker Compose](https://docs.docker.com/compose/install/)

### Установка и запуск

1. Клонируйте репозиторий на локальный компьютер:
   ```
   git clone git@github.com:antonata-c/group_fund.git
   cd group_fund/deploy/
   ```
2. Создайте файл `.env` в корневой директории проекта и добавьте в него переменные окружения по примеру в файле .env.example

3. Запустите контейнеры с помощью Docker Compose:
   ```
   docker-compose up
   ```
4. Примените миграции, соберите статику и заполните базу:
   ```
    sudo docker compose exec -it backend bash
   
    python manage.py migrate --noinput
   
    python manage.py collectstatic --noinput
   ```
5. При необходимости создайте суперпользователя заполните базу тестовыми данными:
   ```
   python manage.py createsuperuser

   python manage.py fillbase --users 10 --collects 10 --payments 10
   ```
6. Для запуска тестирования:
   ```
   python manage.py test
   ```
#### Приложение будет доступно по адресу:

**http://127.0.0.1/**

#### Документация Swagger доступна по адресу:

**http://127.0.0.1/api/swagger/**

<details>
<summary>Данные по Coverage</summary>
<pre>
Name                                                                     Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------------
api/__init__.py                                                              0      0   100%
api/apps.py                                                                  4      0   100%
api/urls.py                                                                  2      0   100%
api/v1/__init__.py                                                           0      0   100%
api/v1/permissions.py                                                        6      1    83%   11
api/v1/serializers.py                                                       42      1    98%   32
api/v1/tests/__init__.py                                                     0      0   100%
api/v1/tests/test_serializers.py                                            28      0   100%
api/v1/tests/test_views.py                                                  53      0   100%
api/v1/urls.py                                                               8      0   100%
api/v1/views.py                                                             45      1    98%   66
config/__init__.py                                                           2      0   100%
config/celery.py                                                             6      0   100%
config/settings.py                                                          44      1    98%   69
config/urls.py                                                               5      0   100%
fund/__init__.py                                                             0      0   100%
fund/admin.py                                                               13      0   100%
fund/apps.py                                                                 5      0   100%
fund/constants.py                                                            4      0   100%
fund/factories.py                                                           27      0   100%
fund/management/__init__.py                                                  0      0   100%
fund/management/commands/__init__.py                                         0      0   100%
fund/management/commands/fillbase.py                                        20      0   100%
fund/migrations/0001_initial.py                                              7      0   100%
fund/migrations/0002_alter_collect_end_date.py                               5      0   100%
fund/migrations/0003_rename_author_collect_user_alter_collect_image.py       4      0   100%
fund/migrations/0004_remove_collect_current_amount.py                        4      0   100%
fund/migrations/__init__.py                                                  0      0   100%
fund/models.py                                                              33      1    97%   44
fund/tasks.py                                                                6      1    83%   8
fund/tests/__init__.py                                                       0      0   100%
fund/tests/test_commands.py                                                  9      0   100%
fund/tests/test_models.py                                                   25      0   100%
manage.py                                                                   12      2    83%   12-13
------------------------------------------------------------------------------------------------------
TOTAL                                                                      419      8    98%
</pre>
</details>


## Автор проекта

**[Антон Земцов](https://github.com/antonata-c)**
