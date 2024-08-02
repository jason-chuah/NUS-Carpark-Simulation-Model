
FROM python:3.10.6-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=flask1.py
CMD ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
