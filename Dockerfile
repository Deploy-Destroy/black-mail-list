FROM python:3.14

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt

EXPOSE 5000

# Ejecuta la aplicación
CMD ["python3", "application.py"]


##Confguración New Relic
# RUN pip install newrelic
# ENV NEW_RELIC_APP_NAME="docker"
# ENV NEW_RELIC_LOG=stdout
# ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
#INGEST_License
# ENV NEW_RELIC_LICENSE_KEY=65a325f6caf10c382251dce69df2eaabFFFFNRAL
# ENV NEW_RELIC_LOG_LEVEL=info
# etc.

#ENTRYPOINT ["newrelic-admin", "run-program"]
