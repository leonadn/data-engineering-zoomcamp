# data-engineering-zoomcamp
To learn data engineering

This can be found in: https://github.com/leonadn/data-engineering-zoomcamp


Link to github of the course: https://github.com/DataTalksClub/data-engineering-zoomcamp



This data contains taxi trips in usa:
https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
First data set adress:
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet


# fetching data bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet



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


# LOG IN VIA POSTGRES CLIENT (PGCLI): 
pgcli -h localhost -u root -d ny_taxi 

# FOr postGres port 5432 is default BUT could be something else:
pgcli -h localhost -p 5432 -u root -d ny_taxi

# to use PGcli:
conda create --no-default-packages -n test_pgcli python
conda activate test_pgcli
conda install -n test_pgcli -c conda-forge pgcli

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

# convert notebook to script 

jupyter nbconvert --to=script from_data_set_to_posgres.ipynb




################################ Re-do everything

# Remove network
docker network ls

# Find network to remove (ID)
docker network rm f8f0586e9772

# Start network:
docker network create pg-network




# In order to list the Docker containers, we can use the 
docker ps
# or 
docker container ls
# In order to list images:
docker images

# List all containers
docker ps -a

# Remove container (not the iamge):
docker rm postgresql

# Start database
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




# Run script with 

    python ingest_data.py\
        --user=root\
        --password=root\
        --host=localhost\
        --port=5432\
        --db=ny_taxi\
        --table_name=yellow_taxi_data\
        --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet


############################

# Remove network
docker network ls

# Find network to remove (ID)
docker network rm f8f0586e9772

# Start network:
docker network create pg-network




# In order to list the Docker containers, we can use the 
docker ps
# or 
docker container ls
# In order to list images:
docker images

# List all containers
docker ps -a

# Remove container (not the iamge):
docker rm postgresql

# Start database
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


# Next build a docker for ingest_dsata.py, see docker_ingest ... run it:
docker run -it --network=pg-network ingest:tagger         --user=root\
        --password=root\
        --host=postgresql\
        --port=5432\
        --db=ny_taxi\
       --table_name=yellow_taxi_data\
        --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet



# make sure the inparameters to the docker (to the script in the docker) uses host=postgresql 
# (its not localhost anymore since the docker you are in does not have the same localhost as your computer).



##################################################### DOCKER COMPOSE
# Instead of doing all this:

# Start network:
docker network create pg-network

# Start database
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

# docker_ingest:
docker run -it --network=pg-network ingest:tagger         --user=root\
        --password=root\
        --host=postgresql\
        --port=5432\
        --db=ny_taxi\
       --table_name=yellow_taxi_data\
        --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet


# Do everything at once with docker compose:

version: "3.0" # For some reasone you need a version here
services:
  pgdatabase:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./2_docker_SQL/ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
  docker_ingest:
    build: ./docker_ingest
    command:
      - "--user=root"
      - "--password=root"
      - "--host=pgdatabase"
      - "--port=5432"
      - "--db=ny_taxi"
      - "--table_name=yellow_taxi_data"
      - "--url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

# No network is needed.

# Start docker compose:
docker-compose up

# Stop
docker-compose down 
# or
Crl + C














# TERRAFORMA AND GCP 1.3.1

export GOOGLE_APPLICATION_CREDENTIALS=/Users/leonandersson/Downloads/dtc-de-358410-f41cfaae93a8.json
# I moved it :
/Users/leonandersson/GCloud-credentials/dtc-de-358410-f41cfaae93a8.json

# Download Terraform 
brew tap hashicorp/tap
brew install hashicorp/tap/terraform


# Create Two resources in the google invirment 
# 1. Google Cloud Storage 
# 2. BigQuery 

# Seperet services for terraform and another for our pipline 

# Activate API 
https://console.cloud.google.com/apis/api/iam.googleapis.com/metrics?project=dtc-de-358410&authuser=1
https://console.cloud.google.com/apis/api/iamcredentials.googleapis.com/metrics?project=dtc-de-358410&authuser=1




# LOG IN to pgadmin:

  pgdatabase: <---------------------------------- this is the name 
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=root <-------------------------use 
      - POSTGRES_PASSWORD=root <-----pass
      - POSTGRES_DB=ny_taxi <-- this is autmatic
    volumes:
      - "./2_docker_SQL/ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"


# open GUI pgadim
localhost 8080
# Close this one before restart




# home work
select count(*) FROM yellow_taxi_data 
where tpep_dropoff_datetime::date = '2021-01-15';
51977


# TODO:
FREDAG:
istället för att göra vm machine for google ... det kostar nog pengar. 
gör det på din dator hemma istället :) 
SÅ 1.4.1
och igen testa lite på 1.4.2
Sen är du klar med kappitel 1 (week 1)




# VM machine 1.4.1
 # 1. Create ssh key for machine 
 ssh-keygen -t rsa -f gcp_course -C "leonadn" -b 2048
 # pass: EMPTY as in nothing 
 # It creates two keys:
gcp_course (private)
gcp_course.pub (public)
# 2. put public key to google cloud and create machine.
# GO to to meta data and add ssh-key
# Go to VM instance and create machine
# ubuntu 20.04 20gb
# Bulid
# copy ssh key the machine is given
# go back to your computer and 
ssh -i ~/.ssh/gcp_course leonadn@35.240.71.31

# you create config for ssh
# just now run
ssh de-zoomcamp
# install docker (sudo apt-get update .... sudo apt-get docker.io) and make ut run without sudo


# when you stop the VM you will get a new IP when restarted.
# The vm is stopped. the only thing that you will be charge with is the storage ... he said a few cents per month ... ok so top 11kr per month max 33kr in total. 


# You should start at week 2. 





# Konto hos amazon 
user: leondavidandersson@gmail.com  
pass: Leon@amazon1234
