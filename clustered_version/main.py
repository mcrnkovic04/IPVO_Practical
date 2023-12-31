import atexit
import psycopg2
from faker import Faker
import time
import random

def cleanup():
    conn = psycopg2.connect(
        host="postgres",
        user="postgres",
        password="password",
        database="mydatabase"
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS clustered_table;")
    conn.commit()

    cursor.close()
    conn.close()

atexit.register(cleanup)
conn = psycopg2.connect(
    host="postgres",  
    user="postgres",
    password="password",
    database="mydatabase"
)

cursor = conn.cursor()

cursor.execute("CREATE TABLE clustered_table (id SERIAL PRIMARY KEY, name VARCHAR);")
conn.commit()

fake = Faker()

for _ in range(1000):
    name = fake.name()
    cursor.execute("INSERT INTO clustered_table (name) VALUES (%s);", (name,))

conn.commit()

total_requests = 100
read_percentage = 80  
write_percentage = 100 - read_percentage

cache = {}

cache_hits = 0
cache_misses = 0

start_time = time.time()

for _ in range(total_requests):
    if random.randint(1, 100) <= read_percentage:
        key_to_read = fake.random_int(min=1, max=1000)
        if key_to_read in cache:
            cache_hits += 1
            print(f"Read - Cache Hit: {key_to_read}")
        else:
            cursor.execute("SELECT * FROM clustered_table WHERE id = %s;", (key_to_read,))
            result = cursor.fetchall()
            cache[key_to_read] = result
            cache_misses += 1
            print(f"Read - Cache Miss: {key_to_read}")
    else:
        name_to_write = fake.name()
        cursor.execute("INSERT INTO clustered_table (name) VALUES (%s);", (name_to_write,))
        conn.commit()
        print(f"Write - Name Written: {name_to_write}")

end_time = time.time()
total_time = end_time - start_time

print(f"Total time for OLTP workload with clustered tables (including cache): {total_time} seconds")
print(f"Total Cache Hits: {cache_hits}")
print(f"Total Cache Misses: {cache_misses}")
print(f"Total Requests: {total_requests}")

cursor.close()
conn.close()
