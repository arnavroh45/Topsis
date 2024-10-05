FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install --no-cache-dir django pandas
COPY . /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]