#!/usr/bin/env python
# coding: utf-8


from sqlalchemy import create_engine
from time import time

import argparse
import os
import pandas as pd


def main(params):
    
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    trip_data_table_name = params.trip_data_table_name
    zones_data_table_name = params.zones_data_table_name

    trip_data_url = params.trip_data_url
    zones_data_url = params.zones_data_url

    # Taxi Trip Data
    if trip_data_url.endswith('.csv.gz'):
        trip_data_csv_name = 'output_taxi_trip.csv.gz'
    else:
        trip_data_csv_name = 'output_taxi_trip.csv'

    os.system(f"wget {trip_data_url} -O {trip_data_csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


    trip_df_iter = pd.read_csv(trip_data_csv_name, iterator=True, chunksize=100000)
    trip_df = next(trip_df_iter)

    trip_df.lpep_pickup_datetime = pd.to_datetime(trip_df.lpep_pickup_datetime)
    trip_df.lpep_dropoff_datetime = pd.to_datetime(trip_df.lpep_dropoff_datetime)


    trip_df.head(n=0).to_sql(name=trip_data_table_name, con=engine, if_exists='replace')
    trip_df.to_sql(name=trip_data_table_name, con=engine, if_exists='append')

    
    # Zones Trip Data
    if zones_data_url.endswith('.csv.gz'):
        zones_data_csv_name = 'output_zones.csv.gz'
    else:
        zones_data_csv_name = 'output_zones.csv'

    os.system(f"wget {zones_data_url} -O {zones_data_csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


    zones_df_iter = pd.read_csv(zones_data_csv_name, iterator=True)
    zones_df = next(zones_df_iter)

    zones_df.head(n=0).to_sql(name=zones_data_table_name, con=engine, if_exists='replace')
    zones_df.to_sql(name=zones_data_table_name, con=engine, if_exists='append')


    while True: 
        zones_df = next(zones_df_iter)
        zones_df.to_sql(name=zones_data_table_name, con=engine, if_exists='append')
        print("===="*5)
        print(f"Inserted zones data into Zones Table")
        print("===="*5)

        trip_df = next(trip_df_iter)
        trip_df.lpep_pickup_datetime = pd.to_datetime(trip_df.lpep_pickup_datetime)
        trip_df.lpep_dropoff_datetime = pd.to_datetime(trip_df.lpep_dropoff_datetime)
            
        trip_df.to_sql(name=trip_data_table_name, con=engine, if_exists='append')
        print("===="*5)
        print(f"Inserted trips data into Taxi Trips Table")
        print("===="*5)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--trip_data_table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--zones_data_table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--trip_data_url', required=True, help='url of the trip data csv file')
    parser.add_argument('--zones_data_url', required=True, help='url of the zones data csv file')

    args = parser.parse_args()

    main(args)