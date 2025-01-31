FROM tensorflow/tensorflow:2.15.0-gpu

WORKDIR /app
COPY analysis/ml_models/requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements-ml.txt

COPY analysis/ml_models/ /app/ml_models/

RUN python -c "from transformers import BertTokenizer; BertTokenizer.from_pretrained('bert-base-uncased')"

ENTRYPOINT ["python", "ml_models/model_server.py"]
