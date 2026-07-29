FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -S -g 10001 app \
    && adduser -S -D -H -u 10001 -G app app

COPY --chown=app:app main.py ./main.py

USER app

CMD ["python", "/app/main.py"]
