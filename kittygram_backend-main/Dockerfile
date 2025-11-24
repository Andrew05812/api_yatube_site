FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "kittygram_backend.wsgi:application", "--bind", "0.0.0.0:8000"]

