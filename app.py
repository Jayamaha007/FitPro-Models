from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn import run

# Import the FastAPI apps
from meal import meal
from workout import workout
from tracker import tracker
from detect import dimensions
from plan import  plan

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:8000",  # Replace with the origin of your React app
    "http://localhost:3000",  # Add your frontend origin
    "http://localhost:5000",  # Add your frontend origin
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
app.mount("/body", dimensions)
app.mount("/plan", plan)


@app.options("/{path:path}")
async def handle_options(request):
    return JSONResponse(content="ok", status_code=200)


if __name__ == "__main__":
    # Run the FastAPI app on port 8000
    run(app, host="0.0.0.0", port=8000)
