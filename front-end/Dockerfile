FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
RUN apk update && apk add --no-cache gcc g++ python3-dev unixodbc-dev
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
