drop table if exists items;
drop table if exists users;
drop table if exists bids;
drop table if exists categories;

CREATE TABLE items (
	itemID INTEGER NOT NULL,
	name TEXT NOT NULL,
	currently REAL NOT NULL,
	sellerID VARCHAR NOT NULL,
	buy_price REAL,
	first_bid REAL NOT NULL,
	number_of_bids INTEGER NOT NULL,
	started DATETIME NOT NULL,
	end DATETIME NOT NULL,
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

CREATE TABLE bids (
	itemID INTEGER NOT NULL,
	userID VARCHAR NOT NULL,
	amount REAL NOT NULL,
	time DATETIME NOT NULL,
	FOREIGN KEY(itemID) REFERENCES items(itemID)
	FOREIGN KEY(userID) REFERENCES users(userID)
);
