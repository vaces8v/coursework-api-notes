# Используем официальный образ Python в качестве базового
FROM python:3.12

# Установим необходимые утилиты
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Установим Poetry
RUN pip install poetry

# Установим рабочую директорию
WORKDIR /app

# Копируем файлы конфигурации Poetry и устанавливаем зависимости
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-dev && poetry add python-jose

# Копируем исходный код приложения
COPY ./ /

# Открываем порт, на котором будет работать FastAPI
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]