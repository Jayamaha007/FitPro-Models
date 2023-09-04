from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Load the model and encoder
loaded_model = joblib.load('Models/TrackerResults.joblib')
encoder = joblib.load('Models/TrackEncoder.joblib')

# Store the unique categories and feature names for 'Sex' and 'Activity_Level'
sex_categories = encoder.categories_[0].tolist()
activity_categories = encoder.categories_[1].tolist()
feature_names = encoder.get_feature_names_out(['Sex', 'Activity_Level'])

tracker = FastAPI()


class UserInput(BaseModel):
    Height: int
    Weight: int
    Age: int
    Sex: str
    Activity_Level: str
    Maintenance_Calories: int


@tracker.post("/predict/tracker")
def predict_result(user_input: UserInput):
    # Check if user input categories are in the stored categories
    if user_input.Sex not in sex_categories or user_input.Activity_Level not in activity_categories:
        raise HTTPException(status_code=400, detail="Invalid category provided")

    # Create a DataFrame with the user input
    user_input_df = pd.DataFrame([user_input.dict()])

    # Encode user input using the stored feature names
    user_input_encoded = encoder.transform(user_input_df[['Sex', 'Activity_Level']])
    user_input_features = pd.concat([user_input_df[['Height', 'Weight', 'Age', 'Maintenance_Calories']],
                                     pd.DataFrame(user_input_encoded.toarray(), columns=feature_names)],
                                    axis=1)

    # Predict the result
    predicted_result = loaded_model.predict(user_input_features)

    return {"Predicted_Result": predicted_result[0]}
