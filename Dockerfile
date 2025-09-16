# Базовый образ Python
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска приложения (можно seed.py отдельно)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
