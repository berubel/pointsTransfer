FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /pointsTransfers

COPY requirements.txt requirements.txt
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]