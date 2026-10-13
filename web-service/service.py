from flask import Flask, jsonify, request

app = Flask(__name__)

# Метаболический эквивалент (MET): id -> (название, MET)
ACTIVITIES = {
    "running":   ("Бег", 9.8),
    "walking":   ("Ходьба", 3.5),
    "cycling":   ("Велосипед", 7.5),
    "swimming":  ("Плавание", 6.0),
    "yoga":      ("Йога", 2.5),
    "strength":  ("Силовая тренировка", 5.0),
    "hiit":      ("Интервальная тренировка", 8.0),
    "rowing":    ("Гребля", 7.0),
    "jump_rope": ("Скакалка", 11.0),
    "dancing":   ("Танцы", 5.0),
}


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/activities")
def activities():
    return jsonify([{"id": k, "name": v[0], "met": v[1]} for k, v in ACTIVITIES.items()])


@app.get("/calories")
def calories():
    activity = request.args.get("activity", "")
    if activity not in ACTIVITIES:
        return jsonify(error="Неизвестный вид активности"), 400
    try:
        weight = float(request.args["weight"])
        minutes = float(request.args["minutes"])
    except (KeyError, ValueError):
        return jsonify(error="Укажите вес и длительность числами"), 400
    if weight <= 0 or minutes <= 0:
        return jsonify(error="Вес и длительность должны быть больше нуля"), 400

    name, met = ACTIVITIES[activity]
    # ккал = MET * вес (кг) * время (ч)
    kcal = round(met * weight * minutes / 60, 1)
    return jsonify(activity=activity, name=name, met=met, calories=kcal)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
