from fastapi import FastAPI
from fastapi.responses import JSONResponse
from uvicorn import run

# Import the FastAPI apps
from meal import meal
from workout import workout
from tracker import tracker

app = FastAPI()

# Include the meal and workout apps under different paths
app.mount("/meal", meal)
app.mount("/workout", workout)
app.mount("/tracker", tracker)

if __name__ == "__main__":
    # Run the FastAPI app on port 8000
    run(app, host="0.0.0.0", port=8000)
