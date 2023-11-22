FROM python:3.9-alpine

WORKDIR /app

RUN apk add gcc libc-dev linux-headers git docker openrc docker-compose

COPY requirements.txt .

RUN git clone https://github.com/kazet/wpgarlic.git wpgarlic

RUN pip install -r wpgarlic/requirements.txt

RUN pip install -r requirements.txt

COPY .. .

RUN sh ./wpgarlic_postinstall.sh

CMD [ "uvicorn", "app:app" , "--host", "0.0.0.0"]
