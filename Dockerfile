FROM redis:7-alpine

WORKDIR /app

COPY --chown=redis:redis main.sh ./main.sh

RUN chmod 0555 /app/main.sh

USER redis

ENTRYPOINT ["/app/main.sh"]
