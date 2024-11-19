# Страховой калькулятор API
## Описание

Этот проект представляет собой REST API сервис для расчёта стоимости страхования в зависимости от типа груза и объявленной стоимости (ОС). Сервис использует актуальные тарифы, которые загружаются из базы данных и рассчитываются на основе типа груза и даты.

## API реализован с использованием 
- FastAPI 
- SQLAlchemy ORM
- PostgreSQL 
- Docker и Docker Compose

## Установка
### 1. Клонируйте репозиторий
    git clone https://github.com/ArtemLiceum/InsuranceService 
    cd insurance-api
### 2. Создайте и активируйте виртуальное окружение
    python -m venv venv
    venv\Scripts\activate
### 3. Установите зависимости
    pip install -r requirements.txt
### 4. Запустите проект с помощью Docker
    docker-compose up --build