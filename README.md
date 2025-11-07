# Проверка работоспособности API-сервиса для учёта инцидентов

<h2>Команды в терминале Linux для запуска и проверки:</h2>

Добавляем в корневую папку .env файл с данными для БД
```bash
# .env
DB_USER=root
DB_PASS=pass
DB_NAME=incidents_db
DB_HOST=db
DB_PORT=3306
```

Сборка проекта и запуск контейнеров
```bash
docker compose up -d --build
```

Создание инцидента
```bash
curl -X POST http://localhost:5000/incidents \
  -H "Content-Type: application/json" \
  -d '{"description": "Самокат не в сети", "source": "monitoring"}'
```

Список всех инцидентов
```bash
curl http://localhost:5000/incidents
```

Список инцидентов с фильтром по статусу new
```bash
curl http://localhost:5000/incidents?status=new
```

Изменение статуса инцидента на resolved
```bash
curl -X PATCH http://localhost:5000/incidents/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```
