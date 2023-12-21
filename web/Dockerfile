FROM python:3.9-alpine

WORKDIR /app

COPY ..api/ .

RUN apk add gcc libc-dev linux-headers

# We copy just the requirements.txt first to leverage Docker cache and speed up builds on code changes
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
