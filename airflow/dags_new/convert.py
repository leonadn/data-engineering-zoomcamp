import pandas as pd
# this task doesn't do anything.
def parquet2csv_task(parquet_file, csv_file):
    print(f"Start converting from {parquet_file} to {csv_file}")
    df = pd.read_parquet(parquet_file) # for some reason this is not parquet??? This task does nothing.
    #df = pd.read_csv(parquet_file)
    print("#################### PRINT DF ##################")
    print(df)
    df.to_csv(csv_file)
    print(f"Done converting from {parquet_file} to {csv_file}")