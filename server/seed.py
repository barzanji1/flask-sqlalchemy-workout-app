#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():

    # Clear existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Create exercises
    push_ups = Exercise(
        name='Push Ups',
        category='Strength',
        equipment_needed=False
    )

    squats = Exercise(
        name='Squats',
        category='Strength',
        equipment_needed=False
    )

    treadmill = Exercise(
        name='Treadmill',
        category='Cardio',
        equipment_needed=True
    )

    db.session.add_all([
        push_ups,
        squats,
        treadmill
    ])

    # Create workouts
    workout_one = Workout(
        date=date(2026, 9, 25),
        duration_minutes=45,
        notes='Upper body and cardio workout'
    )

    workout_two = Workout(
        date=date(2026, 9, 24),
        duration_minutes=30,
        notes='Lower body workout'
    )

    db.session.add_all([
        workout_one,
        workout_two
    ])

    # Flush so IDs are available before creating join records
    db.session.flush()

    # Connect exercises to workouts
    workout_exercise_one = WorkoutExercise(
        workout_id=workout_one.id,
        exercise_id=push_ups.id,
        reps=12,
        sets=3
    )

    workout_exercise_two = WorkoutExercise(
        workout_id=workout_one.id,
        exercise_id=treadmill.id,
        duration_seconds=900
    )

    workout_exercise_three = WorkoutExercise(
        workout_id=workout_two.id,
        exercise_id=squats.id,
        reps=15,
        sets=4
    )

    db.session.add_all([
        workout_exercise_one,
        workout_exercise_two,
        workout_exercise_three
    ])

    db.session.commit()

    print('Database seeded successfully!')