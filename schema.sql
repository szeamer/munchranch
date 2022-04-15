DROP TABLE IF EXISTS cats;
CREATE TABLE cats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    catname TEXT NOT NULL,
    sex TEXT NOT NULL CHECK (sex='male' OR sex='female'),
    color TEXT,
    about TEXT,
    forsale INTEGER, 
    picture TEXT,
    breeding INTEGER, 
    birthdate DATE,
    sold INTEGER
);

DROP TABLE IF EXISTS litters;
CREATE TABLE litters (
    father TEXT NOT NULL,
    mother TEXT NOT NULL,
    birthdate DATE,
    FOREIGN KEY (father) REFERENCES cats(id),
    FOREIGN KEY (mother) REFERENCES cats(id),
    PRIMARY KEY (father, mother, birthdate)
);

DROP TABLE IF EXISTS belongs;
CREATE TABLE belongs (
    father TEXT NOT NULL,
    mother TEXT NOT NULL,
    birthdate DATE NOT NULL,
    kitten TEXT NOT NULL,
    FOREIGN KEY (kitten) REFERENCES cats(id),
    FOREIGN KEY (father, mother, birthdate) REFERENCES litters(father, mother, birthdate)
);


INSERT INTO cats (catname, sex, color, about, forsale, breeding, birthdate) VALUES ('Furtrout', 'female', 'seal point', 'Furtrout is the ery best cat', 0, 1, 2011-01-04);
INSERT INTO cats (catname, sex, color, about, forsale, breeding, birthdate) VALUES ('Sunfoot', 'male', 'ginger', 'Nice sunny kitty cat', 0, 1, 2017-05-14);
INSERT INTO cats (catname, sex, color, about, forsale, breeding, birthdate) VALUES ('Fish', 'female', 'seal point', 'Furtrout is the ery best cat', 0, 1, 2020-04-20);
INSERT INTO cats (catname, sex, color, about, forsale, breeding, birthdate) VALUES ('Soot', 'male', 'black', 'Nice sunny kitty cat', 0, 1, 2022-01-02);
INSERT INTO cats (catname, sex, color, about, forsale) VALUES ('Fishcat', 'female', 'standard', 'Soft and good cat.', 0);
INSERT INTO cats (catname, sex, color, about, forsale) VALUES ('Mitten', 'male', 'grey with white feet, very rare', 'Fluffer who likes fish and plays with everyone. Once he found a cat under the stairs and licked its ears. He is very soft.', 0);

INSERT INTO  litters (father, mother, birthdate) VALUES (2, 1, '2022-01-01');

INSERT INTO belongs (father, mother, birthdate, kitten) VALUES (2, 1, '2022-01-01', 3);
INSERT INTO belongs (father, mother, birthdate, kitten) VALUES (2, 1, '2022-01-01', 4);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username TEXT PRIMARY KEY NOT NULL,
    email TEXT,
    pwhash TEXT NOT NULL
);