From bitnami/spark:3.1

USER root

RUN apt-get update && apt-get install -y cron vim && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["cron", "-f"]