-- Create a PostgreSQL database
CREATE DATABASE IF NOT EXISTS "${POSTGRES_DB}";

-- Create a PostgreSQL user and set the password
CREATE USER IF NOT EXISTS "${POSTGRES_USER}" WITH PASSWORD '${POSTGRES_PASSWORD}';

-- Grant privileges to the user on the database
ALTER ROLE "${POSTGRES_USER}" SET client_encoding TO 'utf8';
ALTER ROLE "${POSTGRES_USER}" SET default_transaction_isolation TO 'read committed';
ALTER ROLE "${POSTGRES_USER}" SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE "${POSTGRES_DB}" TO "${POSTGRES_USER}";
