CREATE TABLE IF NOT EXISTS workouts (
    id           SERIAL PRIMARY KEY,
    activity     TEXT          NOT NULL,
    duration_min INTEGER       NOT NULL CHECK (duration_min > 0),
    weight_kg    NUMERIC(5,1)  NOT NULL CHECK (weight_kg > 0),
    calories     NUMERIC(8,1)  NOT NULL,
    created_at   TIMESTAMPTZ   NOT NULL DEFAULT now()
);

INSERT INTO workouts (activity, duration_min, weight_kg, calories, created_at) VALUES
    ('Бег',        30, 70.0, 343.0, now() - interval '2 days'),
    ('Плавание',   45, 70.0, 315.0, now() - interval '1 day'),
    ('Йога',       60, 70.0, 175.0, now() - interval '3 hours');
