import argparse
from pydoc import describe
import pandas as pd
from sqlalchemy import create_engine
import os

chunksize = 100000

"""
TO RUN MODULE:
    python ingest_data.py\
        --user=root\
        --password=root\
        --host=localhost\
        --port=5432\
        --db=ny_taxi\
        --table_name=yellow_taxi_data\
        --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
"""

def main(args):
    ingest_data(args)


def ingest_data(args):
    # Create connection to database
    engine = create_engine(f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.db}")

    # Load file
    file_name = "output"
    os.system(f"wget {args.url} -O {file_name}.parquet") # bash
    df = pd.read_parquet(f"{file_name}.parquet")
    df.to_csv(f"{file_name}.csv")

    # Create iterator
    df_iter = pd.read_csv(f"{file_name}.csv", iterator = True, chunksize = chunksize)

    # Iternate and upload
    while (True):
        try: 
            df = next(df_iter)
            print("Trans data")
        except StopIteration:
            # Nothing more to upload
            break
        else:
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name = args.table_name, con = engine, if_exists = "append")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Ingest CSV data to Postgres")

    parser.add_argument("--user", help = "user name for posgres")
    parser.add_argument("--password", help = "password for posgres")
    parser.add_argument("--host", help = "host for posgres")
    parser.add_argument("--port", help = "port for posgres")
    parser.add_argument("--db", help = "database name for posgres")
    parser.add_argument("--table_name", help = "name of the table where we will write the result to")
    parser.add_argument("--url", help = "url of the cvs file")

    args = parser.parse_args()

    main(args)
    