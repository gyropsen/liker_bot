FROM python:3.12-slim

WORKDIR /app

ENV POETRY_VERSION=1.8.2 \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get -y install curl

# Официальный способ установки poetry
# Этот способ позволяет poetry изолировать его зависимости от наших зависимостей.
RUN pip install --upgrade pip  \
    && curl -sSL https://install.python-poetry.org | python3  \
    && poetry config virtualenvs.create false \
    && poetry --version

# Копирование зависимостей poetry в контейнер
COPY poetry.lock pyproject.toml /app/

# Установка poetry
RUN poetry install --no-dev

# Копируем код приложения в контейнер
COPY . .

# Создать папку для логов
CMD ["sh", "-c", "mkdir logs"]

CMD ["sh", "-c", "python3 main.py"]