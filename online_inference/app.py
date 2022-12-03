import pickle
from typing import List
import logging
import json

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import pandas as pd
import uvicorn

from transformer import CustomTransformer


HEALTH_CONDITION = True
PATH_TO_MODEL = 'model.pkl'
PATH_TO_OUTPUT = 'prediction.csv'

logger = logging.getLogger("predict")

app = FastAPI()


HEALTH_CONDITION = True
model = None
transformer = None


class Item(BaseModel):
    data: str


class ModelResponse(BaseModel):
    result: str


@app.get("/")
async def root():
    return {"message": "ML online inference service"}


@app.on_event("startup")
async def startup():
    global transformer
    transformer = CustomTransformer()
    transformer.load_scaler()
    transformer.load_encoder()

    with open('model.pkl', 'rb') as prediction_model:
        global model
        model = pickle.load(prediction_model)
        logging.info('model loaded')


@app.get("/predict/", response_model=ModelResponse)
async def predict(request: Item) -> List:
    df = pd.read_json(request.data)
    logging.info('encoder loaded')
    transformed_df = transformer.transform(df)
    predictions = model.predict(transformed_df)
    str_predictions = list(map(str, predictions))
    result = " ".join(str_predictions)
    return {'result': result}


@app.get("/health", status_code=200)
async def health(response: Response):
    if model is None:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    if transformer is None:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return "model was successfully loaded"


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
