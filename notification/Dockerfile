FROM python:3.9

RUN pip install --upgrade pip
COPY ./ ./
RUN pip install -r requirements.txt
RUN pip install -U drf-yasg
RUN pip install gunicorn
