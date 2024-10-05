FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache gcc musl-dev postgresql-dev postgresql-client

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

WORKDIR /backend

RUN pip install --upgrade pip --no-cache-dir && \
    pip install pipenv --no-cache-dir

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system --ignore-pipfile

COPY . .

RUN chown -R django-user:django-user /backend

USER django-user

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]