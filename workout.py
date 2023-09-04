# workout.py

from fastapi import FastAPI
import joblib
from pydantic import BaseModel

workout = FastAPI()

# Load the trained model
loaded_model = joblib.load('Models/workoutmodel.joblib')


class UserInput(BaseModel):
    age: int
    weight_kg: float
    exercise_hours_per_week: int
    calories_consumed_per_day: int


@workout.post("/predict/workout")
async def recommend(user_input: UserInput):
    try:
        input_data = [
            [
                user_input.age,
                user_input.weight_kg,
                user_input.exercise_hours_per_week,
                user_input.calories_consumed_per_day
            ]
        ]

        recommendation = loaded_model.predict(input_data)

        return {"workout_recommendation": recommendation[0]}

    except Exception as e:
        return {"error": str(e)}
