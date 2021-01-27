DROP TABLE IF EXISTS Gamer CASCADE;

CREATE TABLE Gamer(
id SERIAL PRIMARY KEY UNIQUE,
name TEXT NOT NULL,
login TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
pokemon TEXT[] DEFAULT '{}'
);