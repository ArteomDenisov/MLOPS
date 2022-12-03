FROM python:3.9

COPY requirements.txt app.py model.pkl transformer.py scaler.pkl encoder.pkl /
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]