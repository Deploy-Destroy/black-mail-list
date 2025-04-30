FROM python:3.13-alpine
RUN apk add py3-pip \
&& pip install --upgrade pip
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
WORKDIR /test
RUN pytest --maxfail=1 --disable-warnings --tb=short
WORKDIR /
EXPOSE 5000

CMD ["python", "application.py"]