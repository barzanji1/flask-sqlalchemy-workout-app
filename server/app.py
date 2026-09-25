from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

# Define Routes here
@app.route('/workouts', methods=['GET'])
def workouts():
    workouts = Workout.query.all()

    return make_response(
        workouts_schema.dump(workouts),
        200
    )


@app.route('/workouts/<int:id>', methods=['GET'])
def workout_by_id(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return make_response(
            {'error': 'Workout not found'},
            404
        )

    workout_data = workout_schema.dump(workout)
    workout_data['exercises'] = [
        exercise_schema.dump(exercise)
        for exercise in workout.exercises
    ]

    return make_response(workout_data, 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())

        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return make_response(
            workout_schema.dump(workout),
            201
        )

    except (ValidationError, ValueError) as error:
        db.session.rollback()

        if isinstance(error, ValidationError):
            message = error.messages
        else:
            message = str(error)

        return make_response(
            {'errors': message},
            400
        )


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return make_response(
            {'error': 'Workout not found'},
            404
        )

    db.session.delete(workout)
    db.session.commit()

    return make_response('', 204)


@app.route('/exercises', methods=['GET'])
def exercises():
    exercises = Exercise.query.all()

    return make_response(
        exercises_schema.dump(exercises),
        200
    )


@app.route('/exercises/<int:id>', methods=['GET'])
def exercise_by_id(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_response(
            {'error': 'Exercise not found'},
            404
        )

    exercise_data = exercise_schema.dump(exercise)
    exercise_data['workouts'] = [
        workout_schema.dump(workout)
        for workout in exercise.workouts
    ]

    return make_response(exercise_data, 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())

        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return make_response(
            exercise_schema.dump(exercise),
            201
        )

    except (ValidationError, ValueError) as error:
        db.session.rollback()

        if isinstance(error, ValidationError):
            message = error.messages
        else:
            message = str(error)

        return make_response(
            {'errors': message},
            400
        )


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_response(
            {'error': 'Exercise not found'},
            404
        )

    db.session.delete(exercise)
    db.session.commit()

    return make_response('', 204)


@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def create_workout_exercise(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return make_response(
            {'error': 'Workout not found'},
            404
        )

    if not exercise:
        return make_response(
            {'error': 'Exercise not found'},
            404
        )

    try:
        request_data = request.get_json() or {}

        data = {
            **request_data,
            'workout_id': workout_id,
            'exercise_id': exercise_id
        }

        validated_data = workout_exercise_schema.load(data)

        workout_exercise = WorkoutExercise(**validated_data)

        db.session.add(workout_exercise)
        db.session.commit()

        return make_response(
            workout_exercise_schema.dump(workout_exercise),
            201
        )

    except (ValidationError, ValueError) as error:
        db.session.rollback()

        if isinstance(error, ValidationError):
            message = error.messages
        else:
            message = str(error)

        return make_response(
            {'errors': message},
            400
        )

if __name__ == '__main__':
    app.run(port=5555, debug=True)