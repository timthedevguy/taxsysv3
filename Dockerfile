FROM node:alpine3.10 as builder

RUN mkdir /code
WORKDIR /code
COPY ./package.json /code/

RUN yarn install

FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code
ADD . /code/

COPY --from=builder /code/node_modules /code/node_modules

RUN apt-get update -y && apt-get install -y libpq-dev postgresql-client && pip install --upgrade pip && pip install pipenv && pipenv install --deploy --system && chmod +x /code/docker-entrypoint.sh

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]
