FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

ENV FLASK_APP=backend/app.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "3000"]