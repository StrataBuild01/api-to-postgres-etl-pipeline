API to PostgreSQL ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline that retrieves user data from a REST API, transforms the response into a structured format, and loads the resulting records into a PostgreSQL database.

This project was built as a hands-on introduction to data engineering, with emphasis on API integration, data transformation, database loading, error handling, logging, environment variables, and version control.

Project Overview

The pipeline automates the movement of user data from an external API into a PostgreSQL database.

Pipeline Flow
JSONPlaceholder REST API
          │
          ▼
       Extract
          │
          ▼
      Transform
          │
          ▼
       Validate
          │
          ▼
      PostgreSQL
          │
          ▼
     Stored User Data

The pipeline currently processes 10 user records from the JSONPlaceholder API.

Technologies Used
Python 3.14
Requests — API requests
Psycopg 3 — PostgreSQL database connectivity
python-dotenv — Environment variable management
PostgreSQL 18
Git & GitHub — Version control and project management

How the Pipeline Works
1. Extract

The pipeline sends a GET request to the JSONPlaceholder users endpoint.

response = requests.get(url, timeout=10)
response.raise_for_status()
data = response.json()

A 10-second timeout prevents the pipeline from waiting indefinitely for the API.

HTTP errors are also handled using raise_for_status().

If the request fails, the pipeline logs the error and stops the process safely.

2. Transform

The API returns more information than the database requires.

The transformation stage extracts only the fields needed by the database:

id
name
email
city


3. Load

The transformed records are loaded into PostgreSQL using Psycopg.

The pipeline inserts new records and updates existing records when the same id already exists.

ON CONFLICT (id)
DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    city = EXCLUDED.city;

This prevents duplicate primary-key errors when the pipeline is executed repeatedly.

4. Logging and Error Handling

The pipeline uses Python's logging module to provide visibility into the ETL process.

Example output:

INFO - Starting data pipeline
INFO - API status: 200
INFO - Users transformed: 10
INFO - Connected to PostgreSQL
INFO - Data successfully loaded into PostgreSQL!
INFO - Pipeline completed successfully

The pipeline handles:

API request failures
HTTP errors
Request timeouts
PostgreSQL/database errors

Project Status

Status: Completed — foundational ETL project

The pipeline has been tested successfully and the project is maintained in GitHub.