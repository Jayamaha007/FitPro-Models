from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the model and necessary pre-processing components
loaded_model = joblib.load('Models/trackerResult.joblib')
scaler = StandardScaler()
label_encoder = LabelEncoder()

# Create an instance of the FastAPI app
app = FastAPI()

# Create a Pydantic model for the user input
class UserInput(BaseModel):
    height: float
    weight: float
    age: float
    sex: str
    maintenance_calories: float

# Define an API endpoint to make predictions
@app.post("/track/")
async def predict_weight_status(user_input: UserInput):
    try:
        # Encode the user's sex
        sex_encoded = label_encoder.transform([user_input.sex.upper()])[0]

        # Scale the user's input
        user_input_scaled = scaler.transform([[
            user_input.height,
            user_input.weight,
            user_input.age,
            sex_encoded,
            user_input.maintenance_calories,
        ]])

        # Make a prediction
        prediction = loaded_model.predict(user_input_scaled)[0]

        # Map the prediction back to a meaningful label
        weight_status = {
            0: "You're Losing Weight",
            1: "You're Maintaining Your Weight",
            2: "You're Gaining Weight",
        }

        return {"Predicted Weight Status": weight_status[prediction]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))