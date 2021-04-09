FROM python:3

WORKDIR /usr/src/app
RUN pip install flask
RUN pip instll python-dotenv
COPY . .

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]o