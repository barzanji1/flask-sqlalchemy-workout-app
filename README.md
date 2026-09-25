# Flask SQLAlchemy Workout Application Backend

## Project Description

This project is a backend REST API for a workout tracking application used by personal trainers. The API allows users to create and manage workouts and reusable exercises.

Workouts and exercises have a many-to-many relationship through the `WorkoutExercise` model. This join model stores additional workout-specific information including sets, reps, and exercise duration.

The application was built using Flask, SQLAlchemy, Flask-Migrate, Marshmallow, and SQLite.

## Models

### Exercise

- `id` - Primary key
- `name` - Exercise name
- `category` - Exercise category
- `equipment_needed` - Indicates whether equipment is required

### Workout

- `id` - Primary key
- `date` - Date of the workout
- `duration_minutes` - Total workout duration
- `notes` - Optional workout notes

### WorkoutExercise

Join model connecting workouts and exercises.

- `id` - Primary key
- `workout_id` - Foreign key referencing a workout
- `exercise_id` - Foreign key referencing an exercise
- `reps` - Number of repetitions
- `sets` - Number of sets
- `duration_seconds` - Exercise duration in seconds

## Installation

Clone the repository and enter the project directory:

```bash
git clone git@github.com:barzanji1/flask-sqlalchemy-workout-app.git
cd flask-sqlalchemy-workout-app
```

Install dependencies:

```bash
pipenv install
pipenv shell
```

Enter the server directory:

```bash
cd server
```

Apply the database migrations:

```bash
flask --app app db upgrade head
```

Seed the database with example data:

```bash
python seed.py
```

## Running the Application

From the `server` directory:

```bash
python app.py
```

The API runs locally on port `5555`.

## API Endpoints

### Workouts

`GET /workouts`

Returns all workouts.

`GET /workouts/<id>`

Returns a single workout and its associated exercises.

`POST /workouts`

Creates a new workout.

`DELETE /workouts/<id>`

Deletes a workout.

### Exercises

`GET /exercises`

Returns all exercises.

`GET /exercises/<id>`

Returns a single exercise and its associated workouts.

`POST /exercises`

Creates a new exercise.

`DELETE /exercises/<id>`

Deletes an exercise.

### Workout Exercises

`POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`

Adds an exercise to an existing workout and stores workout-specific information such as reps, sets, and duration.

## Validation

The application uses multiple validation layers to maintain data integrity:

- SQLAlchemy database constraints
- SQLAlchemy model validations
- Marshmallow schema validations

Examples include requiring exercise names, requiring positive workout durations, and preventing negative sets, reps, and durations.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv