#Import the needed libraries
import requests
import psycopg
import os
from dotenv import load_dotenv
load_dotenv()

# -------------------------
# 1. EXTRACT
# -------------------------

url = "https://jsonplaceholder.typicode.com/users"

#Wait for 10 seconds for the API to repsond, after that, stop waiting.
try:
    response = requests.get(url, timeout=10)

    #Reject bad HTTP responses instead of allowing the pipeline to continue with bad or missing data.
    response.raise_for_status()

    #Otherwise, give the desired response
    data = response.json()
    print("API status:", response.status_code)

except requests.exceptions.RequestException as error:
    print("API request failed:", error)
    exit()


# -------------------------
# 2. TRANSFORM
# -------------------------

users = []

for user in data:
    user_data = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "city": user["address"]["city"]
    }

    users.append(user_data)

print("Users extracted:", len(users))

# -------------------------
# 3. LOAD
# -------------------------

connection = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER")
)



cursor = connection.cursor()

for user in users:
    cursor.execute(
        """
        INSERT INTO users (id, name, email, city)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            city = EXCLUDED.city;
;
        """,
        (
            user["id"],
            user["name"],
            user["email"],
            user["city"]
        )
    )

connection.commit()
#Confirm that the data is loaded successfull

print("Data successfully loaded into PostgreSQL!")

cursor.close()
connection.close()