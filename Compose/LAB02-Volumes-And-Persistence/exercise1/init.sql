-- Initialize database for persistence demo

-- Create a table to demonstrate persistence
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some initial data
INSERT INTO notes (title, content) VALUES 
    ('Docker Volumes', 'Docker volumes provide persistent storage for containers'),
    ('Named Volumes', 'Named volumes are managed by Docker and can be shared between containers'),
    ('Bind Mounts', 'Bind mounts link a container path to a host path');

-- Create a function to add a timestamp to demonstrate data was preserved
CREATE OR REPLACE FUNCTION add_timestamp_note() RETURNS void AS $$
BEGIN
    INSERT INTO notes (title, content) 
    VALUES ('Container Started', 'Container was started/restarted at ' || NOW());
END;
$$ LANGUAGE plpgsql;

-- Call the function when the container initializes
SELECT add_timestamp_note(); 