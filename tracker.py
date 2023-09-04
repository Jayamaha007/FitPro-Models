from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the trained model and other preprocessing objects
loaded_model = joblib.load('trackerResult.joblib')
scaler = StandardScaler()
label_encoder = LabelEncoder()

# Define your FAST API app
app = FastAPI()

# Define the input schema using Pydantic
class UserInput(BaseModel):
    height: float
    weight: float
    age: float
    sex: str
    maintenance_calories: float

# Define an endpoint for making predictions
@app.post("/predict/")
async def predict(user_input: UserInput):
    try:
        # Encode the sex input
        sex_encoded = label_encoder.transform([user_input.sex.upper()])[0]

        # Scale the user input
        user_input_scaled = scaler.transform([[
            user_input.height,
            user_input.weight,
            user_input.age,
            sex_encoded,
            user_input.maintenance_calories
        ]])

        # Make predictions using the loaded model
        prediction = loaded_model.predict(user_input_scaled)[0]

        # Define response messages
        if prediction == "You're Gaining Weight":
            response_msg = "You're Gaining Weight"
        elif prediction == "You're Losing Weight":
            response_msg = "You're Losing Weight"
        else:
            response_msg = "You're Maintaining your Weight"

        return {"prediction": response_msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
