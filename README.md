# Фитнес-трекер (вариант 21) Куриленко Павел, студент группы 223-322

Многокомпонентное приложение на Docker Compose: учёт тренировок и расчёт сожжённых калорий по виду активности.

## Компоненты

| Сервис | Технологии | Назначение |
| --- | --- | --- |
| frontend | HTML/CSS/JS, nginx | Веб-интерфейс с двумя кнопками; проксирует `/api/` на backend |
| backend | Python, Flask, gunicorn | REST API, CRUD по тренировкам, запросы к web-service |
| db | PostgreSQL 16 | Дневник тренировок (`db/init.sql` выполняется при первом старте), данные хранятся в volume |
| web-service | Python, Flask | Расчёт калорий: ккал = MET × вес (кг) × время (ч) |

## Запуск

Требуется установленный Docker с Docker Compose.

```bash
docker compose up -d --build
```

Откройте http://localhost:8080

Остановка: `docker compose down`. Остановка с удалением данных БД: `docker compose down -v`.

Пароли БД по умолчанию можно изменить: скопируйте `.env.example` в `.env` и отредактируйте.

## Как пользоваться

- **Рассчитать и сохранить** — backend запрашивает у web-service расчёт калорий и сохраняет тренировку в БД.
- **Показать дневник** — backend читает записи из БД; у каждой записи есть кнопка «Удалить».

## API backend

- `GET /api/activities` — виды активности (из web-service)
- `GET /api/workouts` — список тренировок
- `POST /api/workouts` — `{"activity": "running", "weight_kg": 70, "duration_min": 30}`
- `DELETE /api/workouts/<id>` — удалить запись

## Структура

```
.
├── docker-compose.yml
├── frontend/      (Dockerfile, nginx.conf, index.html)
├── backend/       (Dockerfile, app.py, requirements.txt)
├── db/            (init.sql)
└── web-service/   (Dockerfile, service.py, requirements.txt)
```
