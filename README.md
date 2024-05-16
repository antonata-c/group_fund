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

<details>
<summary><strong>Запуск с использованием Docker</strong></summary>

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
5. При необходимости создайте суперпользователя и заполните базу тестовыми данными:
   ```
   python manage.py createsuperuser
   
   python manage.py fillbase --users 10 --collects 10 --payments 10
   ```
#### Приложение будет доступно по адресу:

**http://127.0.0.1/**

#### Документация Swagger доступна по адресу:

**http://127.0.0.1/api/swagger/**

</details>

<details>
<summary><strong>Локальный запуск через pip</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлен Python и pip. Рекомендуется использовать виртуальное окружение для изоляции зависимостей проекта.

### Установка и запуск

1. Клонируйте репозиторий на локальный компьютер:
   ```
   git clone git@github.com:antonata-c/group_fund.git
   cd group_fund
   ```
2. Создайте файл `.env` в корневой директории проекта и добавьте в него переменные окружения по примеру в файле .env.example
3. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
   ```

4. Установите зависимости:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Запустите проект:
   ```
   python manage.py migrate
   python manage.py runserver
   ```
6. При необходимости создайте суперпользователя и заполните базу данными:
   ```
   python manage.py createsuperuser
   python manage.py fillbase --users 10 --collects 10 --payments 10
   ```
#### Приложение будет доступно по адресу:

**http://127.0.0.1:8000**

#### Документация Swagger доступна по адресу:

**http://127.0.0.1:8000/swagger/**
   

</details>

## Автор проекта

**[Антон Земцов](https://github.com/antonata-c)**
