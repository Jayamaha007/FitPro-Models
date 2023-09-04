# main.py

from fastapi import FastAPI
#from tracker import app  # Import the FastAPI app from workout.py
from workout import  app

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
