
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from modelify.app.controller import ModelifyController
import os
import onnxruntime as rt
from pydantic import BaseModel, create_model
from typing import List, Any
from starlette.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import numpy as np
import logging
from modelify.app.model import Model


def create_fastapi():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost","http://localhost:8080","https://console.modelify.ai","https://modelify.ai"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    BASE_DIR = Path(__file__).resolve().parent
    modelify = ModelifyController()
    model = Model(modelify_path=modelify.model_folder_path, preprocess=modelify.model_preprocess, postprocess=modelify.model_postprocess)


    app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")
    templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request, "modelify":modelify})


    if modelify.model_input_type == "INPUT_LIST":
        Inputs = modelify.inputs_to_pydantic()
        @app.post("/predict", status_code=200)
        async def predict(inputs: List[Inputs]):
            try:
                values = list(map(lambda x: list(x.dict().values()),inputs))
                if modelify.model_path  is None:
                    raise Exception("Model file couldnt find")

                output = model.run(values)

                return {"result":output}
            except Exception as e:
                return {"success": False, "message":str(e)}

    elif modelify.model_input_type == "IMAGE":
        @app.post("/predict", status_code=200)
        async def predict(image: UploadFile = File(...)):
            try:
                extension = image.filename.split(".")[-1] in ("jpg", "jpeg", "png")
                if not extension:
                    raise Exception("Image must be jpg or png format!") 
                if modelify.model_path  is None:
                    raise Exception("Model file couldnt find")

                img = Image.open(BytesIO(await image.read()))
                img = np.array(img.resize((modelify.model_inputs[0]["width"], modelify.model_inputs[0]["height"])))
                #img /= 255.0
                img = img.astype(np.float32)
                img = np.expand_dims(img, 0)       
    
                output = model.run(img)
                return {"result":output}
            except Exception as e:
                logging.error(e, exc_info=True)
                return {"success": False, "message":str(e)}

    return app
