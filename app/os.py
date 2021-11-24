import os 

# For access to global variables in the system
path = os.getenv("Path")
db = os.getenv("MY_DB_URL")
print(db)
