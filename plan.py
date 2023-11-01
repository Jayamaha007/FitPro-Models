from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Initialize the FastAPI app
plan = FastAPI()

# Load the trained model and encoder
model = joblib.load('Models/workoutResults.joblib')
encoder = joblib.load('Models/workoutEncoder.joblib')  # Load your encoder file here


# Define a Pydantic model for the input data
class UserInput(BaseModel):
    age: int
    weight: int
    workout_intensity: int
    calories_burned: int
    risk_level: str


# Define an endpoint to make predictions
@plan.post("/predict/plan")
def predict(user_input: UserInput):
    # Create a DataFrame from the user input
    user_input_df = pd.DataFrame([user_input.dict()])

    # Encode categorical variables using the loaded encoder
    user_input_encoded = encoder.transform(user_input_df[['risk_level']])
    user_input_features = pd.concat([user_input_df[['age', 'weight', 'workout_intensity', 'calories_burned']],
                                     pd.DataFrame(user_input_encoded.toarray(),
                                                  columns=encoder.get_feature_names_out(['risk_level']))],
                                    axis=1)

    # Make predictions
    recommendation = model.predict(user_input_features)

    return {"workout_recommendation": recommendation[0]}
