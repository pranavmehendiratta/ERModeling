drop table if exists item;

drop table if exists users;

drop table if exists bid;

drop table if exists category;

CREATE TABLE item (
itemID INTEGER NOT NULL,
name TEXT NOT NULL,
currently REAL NOT NULL,

sellerID VARCHAR NOT NULL,
buyprice REAL,
firstbid REAL NOT NULL,
numberofbids INTEGER NOT NULL,
started DATETIME NOT NULL,
ends DATETIME NOT NULL,
description TEXT,
PRIMARY KEY(itemID),
FOREIGN KEY(sellerID) REFERENCES users(userID)
);

CREATE TABLE users (
userID VARCHAR NOT NULL,
location VARCHAR,
country VARCHAR,

rating INTEGER NOT NULL,
PRIMARY KEY(userID)
);

CREATE TABLE category (
itemID INTEGER,
category VARCHAR NOT NULL,
PRIMARY KEY(itemID, category),
FOREIGN KEY(itemID) REFERENCES items(itemID)
);

CREATE TABLE bid (

itemID INTEGER NOT NULL,

userID VARCHAR NOT NULL,
amount REAL NOT NULL,

time DATETIME NOT NULL,
FOREIGN KEY(itemID) REFERENCES items(itemID),

FOREIGN KEY(userID) REFERENCES users(userID)
);
