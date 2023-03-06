FROM python:3.9-slim
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]