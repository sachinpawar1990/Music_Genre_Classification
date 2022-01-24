FROM python:3.8-slim-buster
## create directories
RUN mkdir -p /app/input_data
RUN mkdir -p /app/objects
RUN mkdir -p /app/output_data
## copy files
COPY /app/objects/finalized_model.sav /app/objects/finalized_model.sav
COPY /app/objects/model_columns.csv /app/objects/model_columns.csv
COPY /app/objects/scaler.obj /app/objects/scaler.obj
COPY /app/objects/ord_encoder.obj /app/objects/ord_encoder.obj
COPY /app/main.py /app/main.py
COPY /app/model_prediction.py /app/model_prediction.py
COPY /requirements.txt /requirements.txt
## install Python-packages
RUN pip3 install --no-cache-dir -r /requirements.txt
RUN python -m nltk.downloader vader_lexicon
# # Run the Python Script
CMD [ "python", "/app/main.py", "--host=127.0.0.1", "--port=8000"]
EXPOSE 8000
##CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]