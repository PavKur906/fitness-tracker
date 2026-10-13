import os

import psycopg2
import psycopg2.extras
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
WEB_SERVICE_URL = os.environ.get("WEB_SERVICE_URL", "http://web-service:5001")

SELECT_FIELDS = """
    id, activity, duration_min,
    weight_kg::float AS weight_kg,
    calories::float AS calories,
    to_char(created_at, 'DD.MM.YYYY HH24:MI') AS created_at
"""


def query(sql, params=(), fetch=True):
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None
    finally:
        conn.close()


@app.errorhandler(psycopg2.Error)
def db_error(exc):
    app.logger.error("DB error: %s", exc)
    return jsonify(error="Ошибка базы данных"), 500


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.get("/api/activities")
def activities():
    try:
        r = requests.get(f"{WEB_SERVICE_URL}/activities", timeout=5)
        return jsonify(r.json())
    except requests.RequestException:
        return jsonify(error="Web-сервис расчёта недоступен"), 502


@app.get("/api/workouts")
def list_workouts():
    rows = query(f"SELECT {SELECT_FIELDS} FROM workouts ORDER BY id DESC LIMIT 100")
    return jsonify(rows)


@app.post("/api/workouts")
def add_workout():
    data = request.get_json(silent=True) or {}
    try:
        activity = str(data["activity"])
        weight = float(data["weight_kg"])
        minutes = int(data["duration_min"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Заполните все поля корректно"), 400
    if not (20 <= weight <= 300 and 1 <= minutes <= 600):
        return jsonify(error="Вес: 20–300 кг, длительность: 1–600 минут"), 400

    try:
        r = requests.get(
            f"{WEB_SERVICE_URL}/calories",
            params={"activity": activity, "weight": weight, "minutes": minutes},
            timeout=5,
        )
    except requests.RequestException:
        return jsonify(error="Web-сервис расчёта недоступен"), 502
    if r.status_code != 200:
        return jsonify(error=r.json().get("error", "Ошибка расчёта")), 400
    calc = r.json()

    rows = query(
        f"""INSERT INTO workouts (activity, duration_min, weight_kg, calories)
            VALUES (%s, %s, %s, %s) RETURNING {SELECT_FIELDS}""",
        (calc["name"], minutes, weight, calc["calories"]),
    )
    return jsonify(rows[0]), 201


@app.delete("/api/workouts/<int:workout_id>")
def delete_workout(workout_id):
    query("DELETE FROM workouts WHERE id = %s", (workout_id,), fetch=False)
    return jsonify(status="deleted")
