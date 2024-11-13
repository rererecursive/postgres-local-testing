CREATE TABLE IF NOT EXISTS etl.entries  (
    id serial primary key,
    message varchar(512),
    username varchar(64),
    inserted_at timestamp default now()
);

CREATE TABLE IF NOT EXISTS raw.fruit  (
    id serial primary key,
    name varchar(128),
    colour varchar(128),
    age int,
    inserted_at timestamp default now()
);
