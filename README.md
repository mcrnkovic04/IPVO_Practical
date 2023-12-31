Benchmarking System Setup and Instructions
This repository contains code for benchmarking clustered and non-clustered database tables in the context of OLTP read and write workloads.

PostgreSQL: The chosen database system;
Python: Used for scripting and running the benchmark;
Faker: Utilized for generating test data;
Docker: Containerization for easy setup and reproducibility.

Docker Setup
Clone the Repository:
git clone https://github.com/mcrnkovic04/IPVO_Practical.git

cd [repository_directory]

Build Docker Images:
docker-compose build

Run Docker Containers:

docker-compose up -d

Run Benchmarking Code:

For Clustered Database:
docker-compose exec clustered_db python clustered_benchmark.py

For Non-Clustered Database:
docker-compose exec non_clustered_db python non_clustered_benchmark.py

View Results:
Monitor the terminal output for each script to see individual read and write times.
Adjust the number of iterations or any other parameters in the scripts as needed.
