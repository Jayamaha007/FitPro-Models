from fastapi import FastAPI
from fastapi.responses import JSONResponse
import torch
from ultralytics import YOLO
from ultralytics.models.yolo.detect import DetectionPredictor
from fastapi import UploadFile, File
from pydantic import BaseModel
import shutil

model = YOLO('Models/dimensions.pt')

dimensions = FastAPI()


class FileModel(BaseModel):
    file: UploadFile = File(...)


@dimensions.post("/hipwaist")
async def upload_file(file: UploadFile = File(...)):
    with open("saved_file.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("File Saving part Done")

    # Perform inference with your model
    results = model("saved_file.jpg")
    boxes = results[0].boxes
    hip = boxes[1]
    waist = boxes[0]
    hipCords = hip.xywh[0]
    waistCords = waist.xywh[0]
    hip_width = hipCords[2]
    waist_width = waistCords[2]

    ratio = waist_width.item() / hip_width.item()
    rounded_ratio = round(ratio, 2)

    # Return the result as a JSON response
    return {"hip_width": hip_width, "waist_width": waist_width, "hip_waist_ratio": rounded_ratio}
