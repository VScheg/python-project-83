CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS checks (
    id SERIAL PRIMARY KEY,
    status_code BIGINT,
    url_id INT NOT NULL REFERENCES urls(id),
    h1 VARCHAR,
    title VARCHAR,
    description VARCHAR,
    created_at DATE DEFAULT CURRENT_DATE
);