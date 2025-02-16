CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    embedding VECTOR(2)  -- Adjust dimension based on your model
);

CREATE TABLE user_preferences (
    user_id INT,
    movie_id INT,
    interaction_embedding VECTOR(1536)  -- User preference vector
);