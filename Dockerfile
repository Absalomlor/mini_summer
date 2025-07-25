FROM python:3.10

RUN apt-get update && apt-get install -y --no-install-recommends git

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python init_db.py

EXPOSE 8000

CMD ["fastapi", "dev", "main.py"]