from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Initialize the FastAPI app
meal = FastAPI()

# Load the trained model and encoder
model = joblib.load('Models/dietPlan.joblib')
encoder = joblib.load('Models/Dietencoder.joblib')  # Load your encoder file here


# Define a Pydantic model for the input data
class UserInput(BaseModel):
    Age: int
    Gender: str
    Activity: str
    CaloriesIntake: int


# Define an endpoint to make predictions
@meal.post("/predict/meal")
def predict(user_input: UserInput):
    # Create a DataFrame from the user input
    user_input_df = pd.DataFrame([user_input.dict()])

    # Encode categorical variables using the loaded encoder
    user_input_encoded = encoder.transform(user_input_df[['Gender', 'Activity']])
    user_input_features = pd.concat([user_input_df[['Age', 'CaloriesIntake']],
                                     pd.DataFrame(user_input_encoded.toarray(),
                                                  columns=encoder.get_feature_names_out(['Gender', 'Activity']))],
                                    axis=1)

    # Make predictions
    predicted_meal_type = model.predict(user_input_features)

    return {"Predicted_Meal_Type": predicted_meal_type[0]}
