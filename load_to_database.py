#Import the needed libraries
import requests
import psycopg
import os
from dotenv import load_dotenv
import logging
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
# -------------------------
# 1. EXTRACT
# -------------------------


def extract_data():
    """Extract user data from the API."""

    url = "https://jsonplaceholder.typicode.com/users"

    try:
        #Wait for 10 seconds for the API to repsond, after that, stop waiting.
        response = requests.get(url, timeout=10)

        #Reject bad HTTP responses instead of allowing the pipeline to continue with bad or missing data.
        response.raise_for_status()

        #Otherwise, give the desired response
        data = response.json()
        logger.info("API status: %s", response.status_code)
        return data

    except requests.exceptions.RequestException as error:
        logger.error("API request failed: %s", error)
        return None



# -------------------------
# 2. TRANSFORM
# -------------------------

def transform_data(data):
    """Transform the API data into the fields we need."""
    users = []

    for user in data:
        user_data = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "city": user["address"]["city"]
        }

        users.append(user_data)
    logger.info("Users extracted: %s", len(users))
    return users

# -------------------------
# 3. LOAD
# -------------------------
def load_data(users):
    """Load transformed users into PostgreSQL."""
    try:
        connection = psycopg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER")
        )
        logger.info("Connected to PostgreSQL")

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

        logger.info("Data successfully loaded into PostgreSQL!")

        cursor.close()
        connection.close()

    except requests.exceptions.RequestException as error:
        logger.error("API request failed: %s", error)
        return None

# -------------------------
# 4. RUN PIPELINE
# -------------------------

def main():
    """Run the complete data pipeline."""

    logger.info("Starting data pipeline")

    data = extract_data()

    if data is None:
        logger.error("Pipeline stopped because data extraction failed")
        return

    users = transform_data(data)

    load_data(users)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()