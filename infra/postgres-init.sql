-- Initialize PeoplePulse Database

-- Create main database if it doesn't exist
-- (PostgreSQL in Docker will auto-create the database specified in POSTGRES_DB)

-- Create MLflow database for tracking
CREATE DATABASE IF NOT EXISTS mlflow;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Initial setup complete
SELECT 'PeoplePulse database initialized successfully!' AS message;
