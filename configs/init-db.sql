-- Database initialization script for ChatPage project
-- This script runs when PostgreSQL container starts for the first time
-- Uses environment variables for database and user names

-- Create extensions in the default database (specified by POSTGRES_DB)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Create custom functions or procedures here if needed

-- Note: Database and user are created automatically by PostgreSQL container
-- using POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD environment variables
