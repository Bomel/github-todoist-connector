FROM python:3

WORKDIR /usr/src/app
RUN pip install flask python-dotenv requests
COPY . .

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]o