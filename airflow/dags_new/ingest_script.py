import argparse
import time
import pandas as pd
from sqlalchemy import create_engine
import os

chunksize = 100000



def ingest_data(user, password, host, port, db, table_name, csv_file):#, execution_date):
    print(table_name, csv_file)#, execution_date)

    # user = root
    # password = root
    # host = data-engineering-zoomcamp-pgdatabase-1
    # port = 5432
    # db = ny_taxi

    #>>> engine = create_engine(f'postgresql://root:root@data-engineering-zoomcamp-pgdatabase-1:5432/ny_taxi')
    #>>> engine.connect()
    print("############################### ingest_data ###############################")
    print(f"user = {user}")
    print(f"password = {password}")
    print(f"host = {host}")
    print(f"port = {port}")
    print(f"db = {db}")
    print(f"table_name = {table_name}")
    print(f"csv_file = {csv_file}")
    print(f"Running: create_engine('postgresql://{user}:{password}@{host}:{port}/{db}')")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print(f"Then connect: {engine.connect()}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()




    #time.sleep(180)
    #engine = create_engine(f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.db}")

    # Load file
    #file_name = "output"
    #os.system(f"wget {args.url} -O {file_name}.parquet") # bash
    #df = pd.read_parquet(f"{file_name}.parquet")
    #df.to_csv(f"{file_name}.csv")

    # Create iterator
    df_iter = pd.read_csv(csv_file, iterator = True, chunksize = chunksize)

    # Clear table
    df = pd.read_csv(csv_file, nrows = 0)
    df.to_sql(name = table_name, con = engine, if_exists = "replace")
    print(df)

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
            df.to_sql(name = table_name, con = engine, if_exists = "append")


    