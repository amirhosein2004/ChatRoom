-- Database initialization script for ChatPage project
-- This script runs when PostgreSQL container starts for the first time

-- Create additional databases if needed
CREATE DATABASE chatpage_dev;
-- CREATE DATABASE chatpage_test;

-- Connect to the chatpage_dev database to create extensions
\c chatpage_dev;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Create custom functions or procedures here if needed

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE chatpage_dev TO chatpage_user;
