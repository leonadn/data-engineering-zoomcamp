FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow

# Where it goes when it is run
WORKDIR /app

COPY ingest_data.py ingest_data.py

#ENTRYPOINT [ "bash" ] 
# (1)
ENTRYPOINT [ "python" , "ingest_data.py" ] 

# To build:       repository name:tag where to build it
# docker build -t ingest:tagger docker_ingest/

# To run:
# docker run -it ingest:tagger 

# You most run it in the network:
# docker run -it --network=pg-network ingest:tagger

# The database you want to connect to is no longer on localhost, don't do this:
#docker run -it --network=pg-network ingest:tagger         --user=root\
#        --password=root\
#        --host=localhost\ <--------------------- this is wrong
#        --port=5432\
#        --db=ny_taxi\
#        --table_name=yellow_taxi_data\
#        --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet

# DO THIS:
#docker run -it --network=pg-network ingest:tagger         --user=root\
#        --password=root\
#        --host=postgresql\
#        --port=5432\
#        --db=ny_taxi\
#       --table_name=yellow_taxi_data\
#        --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet

# docker ps <-- to list all running docker images
# if not -it => docker ps , docker kill ID