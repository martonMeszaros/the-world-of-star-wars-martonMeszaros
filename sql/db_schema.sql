DROP DATABASE IF EXISTS starwars;

CREATE DATABASE starwars;
\connect starwars;

CREATE TABLE users (
    id SERIAL NOT NULL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    salt CHAR(8) NOT NULL
);

CREATE TABLE planet_votes (
    id SERIAL NOT NULL PRIMARY KEY,
    planet_id INT NOT NULL,
    user_id INT NOT NULL REFERENCES users(id),
    submission_time TIMESTAMP WITHOUT TIME ZONE
);