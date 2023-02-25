## :package: Connecting Postgres database and pgAdmin using Docker
Ingesting data into Postgres database using Docker

### ℹ️ Project Descripton: 
- Automating the connection of pgAdmin and Postgres database server using Docker
- Used Docker **_Compose_** to configure the Postgres database and pgAdmin
- Created a Docker **_Network_** to enable communication between Postgres database and pgAdmin


### 🖥️ Setup
1. Create a Docker Network
```
docker network create <network-name>
```

2. Run Postgres
```
docker run -it \
  -e POSTGRES_USER="<user-name>" \
  -e POSTGRES_PASSWORD="<password>" \
  -e POSTGRES_DB="<database-name-in-Postgres>" \
  -v <whole-path-to-ny_taxi_postgres_data>:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=<docker-network-created-above> \
  --name <host-name> \
  postgres:13
```

3. Run pgAdmin
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="<login-mailID>" \
  -e PGADMIN_DEFAULT_PASSWORD="<password>" \
  -p 8080:80 \
  --network=<docker-network-created-above> \
  --name <connection-name> \
  dpage/pgadmin4
```

4. Connect pgAdmin and Postgres
```
open localhost:8080
login using credentials from pgAdmin
register/create a new server:
	- General: Provide a Server Name
	- Connection: 
		- host: <host-name> from Step 2
		- port: 5432 from Step 2
    - admin: <user-name> from Step 2
    - password: <password> from Step 2
```

### 💉 Data Ingestion

5. Run locally
```
GTAXI="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2021-01.csv.gz"
ZONES="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

python ingest_data.py \
    --user=<user-name> \
    --password=<password> \
    --host=localhost \
    --port=5432 \
    --db=<database-name-in-Postgres-from-Step 2> \
    --trip_data_table_name=green_taxi_trips \
    --zones_data_table_name=taxi_zones \
    --trip_data_url=${GTAXI} \
    --zones_data_url=${ZONES}
```

6. Build a Docker Image
```
docker build -t <image-name> .
```

7. Run with Docker
``` 
GTAXI="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2021-01.csv.gz"
ZONES="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

docker run -it \
  --network=pg-network-homework1 \
  <docker-image-created-above> \
    --user=<user-name> \
    --password=<password> \
    --host=<host-name-Step 2> \
    --port=5432 \
    --db=<database-name-in-Postgres-from-Step 2> \
    --trip_data_table_name=green_taxi_trips \
    --zones_data_table_name=taxi_zones \
    --trip_data_url=${GTAXI} \
    --zones_data_url=${ZONES}
```

### 🎵 Docker Compose

8. Run with Docker Compose
```
# Starting the server
docker-compose up -d

# Stopping the server
docker-compose down
```

### 🗑️ Remvoing the Docker Container
```
# List the containers running
> docker ps

# Stop the container
> docker stop CONTAINER_ID

# Remove the container
> docker rm CONTAINER_ID
```
