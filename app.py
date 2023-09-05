from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn import run

# Import the FastAPI apps
from meal import meal
from workout import workout
from tracker import tracker

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",  # Replace with the origin of your React app
    # Add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)

# Include the meal and workout apps under different paths
app.mount("/meal", meal)
app.mount("/workout", workout)
app.mount("/tracker", tracker)

if __name__ == "__main__":
    # Run the FastAPI app on port 8000
    run(app, host="0.0.0.0", port=8000)
