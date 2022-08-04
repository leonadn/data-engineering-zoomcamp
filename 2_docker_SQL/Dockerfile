FROM python:3.9

RUN pip install pandas

# Where it goes when it is run
WORKDIR /app

COPY pipeline.py pipeline.py

#ENTRYPOINT [ "bash" ] # (1)
ENTRYPOINT [ "python" , "pipeline.py" ] 
# (2)

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

#docker run -it \
 #   -e POSTGRES_USER="root" \
  #  -e POSTGRES_PASSWORD="root" \
   # -e POSTGRES_DB="ny_taxi" \
    #-v $(pwd)/2_docker_SQL/ny_taxi_postgres_data:/var/lib/postgresql/data \
    #-p 5432:5432 \
    #postgres:14-alpine


# LOG IN VIA POSTGRES CLIENT (PGCLI): pgcli -h localhost -u root -d ny_taxi 
# LIST ALL TABELS \dt
# LIST ALL ALL TABLES: SELECT * FROM pg_catalog.pg_tables;


# dpage/pgadmin4 PG Admin GUI 

docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
dpage/pgadmin4


# Create postgres container and pgadmin container and connect via docker network

docker network create pg-network

