FROM python:3.9-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["/bin/bash", "-c", "echo 'Befly AI App Starting...' && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
#CMD ["/bin/bash", "-c", "echo 'Befly AI App Starting...' && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]