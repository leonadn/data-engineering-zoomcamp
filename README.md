# data-engineering-zoomcamp
To learn data engineering

This can be found in: https://github.com/leonadn/data-engineering-zoomcamp


Link to github of the course: https://github.com/DataTalksClub/data-engineering-zoomcamp



This data contains taxi trips in usa:
https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
First data set adress:
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet






# To build:
# docker build -t test:pandas 2_docker_SQL/ <--- since you are standing at root

# To run:
# docker run -it test:pandas (1)
# docker run -it test:pandas 1 345 (2) <---- since pipeline has inparameters ... or ask for sys.argv[1]

# docker ps <-- to list all running docker images
# if not -it => docker ps , docker kill ID


# 1.2.2 Postgres
# Map /var/lib/postgressql/data of container to ny_taxi_postgres_data on my computer (otherwise it will forget all data when container restarted)
# how we want to call this database : ny_taxi
# map a port on host (first) to port on container (second)

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/2_docker_SQL/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:14-alpine


# LOG IN VIA POSTGRES CLIENT (PGCLI): pgcli -h localhost -u root -d ny_taxi 
# MAKE SURE U ARE USING CONDA ENV TEST_PGCLI
# LIST ALL TABELS \dt
# LIST ALL ALL TABLES: SELECT * FROM pg_catalog.pg_tables;


# dpage/pgadmin4 PG Admin GUI 

docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
dpage/pgadmin4

##############################################


# Create postgres container and pgadmin container and connect via docker network
# Creates a docker network
docker network create pg-network

# Database 
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/2_docker_SQL/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name postgresql \
    postgres:14-alpine

# PGAdmin GUI
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgAdmin \
dpage/pgadmin4