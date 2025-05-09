CREATE DATABASE freightxchange;

CREATE USER freightxchange_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE freightxchange TO freightxchange_admin;