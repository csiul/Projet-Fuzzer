FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN apk add gcc libc-dev linux-headers

RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
