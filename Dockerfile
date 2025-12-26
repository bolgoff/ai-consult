FROM python:3.11

WORKDIR /app

<<<<<<< HEAD
RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*
=======
RUN apt-get update && apt-get install -y gcc libpq-dev
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

<<<<<<< HEAD
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
=======
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
