CREATE TABLE IF NOT EXISTS admins (
    _id serial PRIMARY KEY,
	name VARCHAR ( 500 ) NOT NULL,
	password VARCHAR ( 500 ) NOT NULL,
	created TIMESTAMP NOT NULL
);

INSERT INTO admins (name, password, created) VALUES ('test', '$2b$12$rkllomdfhjfbnvgkfmavuepV5xkmsQB7CO0jtg1qYKBRVVmz2Hr9q', now());


CREATE TABLE IF NOT EXISTS cargos (
    _id serial PRIMARY KEY,
	name VARCHAR ( 500 ) NOT NULL,
	weight INTEGER NOT NULL,
	weightUnit VARCHAR ( 20 ) NOT NULL,
	quantity INTEGER NOT NULL,
	quantityUnit VARCHAR (20) NOT NULL,
	info VARCHAR ( 1000 ) NOT NULL,
	addedBy INTEGER REFERENCES admins(_id),
    added TIMESTAMP NOT NULL,
    lastModified TIMESTAMP NOT NULL,
    modifiedBy INTEGER REFERENCES admins(_id)
);

INSERT INTO cargos
	(name, weight, weightUnit, quantity, quantityUnit, info, addedBy,
	 added, lastModified, modifiedBy)
VALUES (
	'Cars', 24000, 'kg', 8, 'pcs', '', 1, now(), now(), 1
);

INSERT INTO cargos
	(name, weight, weightUnit, quantity, quantityUnit, info, addedBy,
	 added, lastModified, modifiedBy)
VALUES (
	'Windows', 10000, 'kg', 50, 'pcs', 'Fragile', 1, now(), now(), 1
);

INSERT INTO cargos
	(name, weight, weightUnit, quantity, quantityUnit, info, addedBy,
	 added, lastModified, modifiedBy)
VALUES (
	'Chocolate bars', 12000, 'kg', 80000, 'pcs', '', 1, now(), now(), 1
);

INSERT INTO cargos
	(name, weight, weightUnit, quantity, quantityUnit, info, addedBy,
	 added, lastModified, modifiedBy)
VALUES (
	'Computer parts', 1000, 'kg', 8000, 'pcs', 'Fragile', 1, now(), now(), 1
);

INSERT INTO cargos
	(name, weight, weightUnit, quantity, quantityUnit, info, addedBy,
	 added, lastModified, modifiedBy)
VALUES (
	'Gasoline', 10000, 'kg', 10000, 'l', 'Higly flamable. Require drives with addtional license for dangerous materials.', 1,
	now(), now(), 1
);

INSERT INTO cargos
	(name, weight, weightUnit, quantity, quantityUnit, info, addedBy,
	 added, lastModified, modifiedBy)
VALUES (
	'Smartphones', 1200, 'kg', 3000, 'pcs', 'Fragile', 1, now(), now(), 1
);

CREATE TABLE IF NOT EXISTS drivers (
    _id serial PRIMARY KEY,
	firstName varchar ( 50 ) NOT NULL,
	lastName varchar ( 50 ) NOT NULL,
	phone varchar ( 50 )  NOT NULL,
	email varchar ( 50 ) NOT NULL,
	addedBy INTEGER REFERENCES admins(_id),
    added TIMESTAMP NOT NULL,
    lastModified TIMESTAMP NOT NULL,
    modifiedBy INTEGER REFERENCES admins(_id)
);

INSERT INTO drivers
	(firstName, lastName, phone, email, addedBy, added, lastModified, modifiedBy)
VALUES (
	'Grzegorz', 'Brz??szyczykiewicz', '1234566778', 'a@a.com', 1, now(), now(), 1
);

INSERT INTO drivers
	(firstName, lastName, phone, email, addedBy, added, lastModified, modifiedBy)
VALUES (
	'John', 'Doe', '987654321', 'asdf@asdf.com', 1, now(), now(), 1
);
INSERT INTO drivers
	(firstName, lastName, phone, email, addedBy, added, lastModified, modifiedBy)
VALUES (
	'Random', 'Dude','112233445', 'qwert@asdad.com', 1, now(), now(), 1
);

INSERT INTO drivers
	(firstName, lastName, phone, email, addedBy, added, lastModified, modifiedBy)
VALUES (
	'Foo', 'Bar','8877665544', 'example@domain.com', 1, now(), now(), 1
);

CREATE TABLE IF NOT EXISTS statuses (
    _id serial PRIMARY KEY,
    transportID integer NOT NULL,
    state varchar ( 200 ) NOT NULL,
	begginingOfState TIMESTAMP NOT NULL,
	endOfState TIMESTAMP,
    duration varchar ( 100 ),
	remaining integer NOT NULL,
    eta varchar ( 100 ) NOT NULL,
    coordinates float[] NOT NULL
);

INSERT INTO statuses
	( transportID,state, begginingOfState, endOfState, duration, remaining, eta, coordinates)
VALUES (
	1, 'Waiting for dispatch', now(), now(), '0 days 17 hrs 0 mins', 1234, 'Unknown', '{52.254717669337616, 21.015183348860532}'
);
INSERT INTO statuses
	( transportID,state, begginingOfState, endOfState, duration, remaining, eta, coordinates)
VALUES (
	1, 'Moving', now(), now(), '0 days 17 hrs 0 mins', 1234, '0 days 16 hrs 13mins', '{52.254717669337616, 21.015183348860532}'
);
INSERT INTO statuses
	( transportID,state, begginingOfState, endOfState, duration, remaining, eta, coordinates)
VALUES (
	1, 'Break to sleep', now(), now(), '0 days 17 hrs 0 mins', 1234, '0 days 16 hrs 13mins', '{52.254717669337616, 21.015183348860532}'
);
INSERT INTO statuses
	( transportID,state, begginingOfState, endOfState, duration, remaining, eta, coordinates)
VALUES (
	1, 'Moving', now(), null, null, 1234, '0 days 16 hrs 13mins', '{52.254717669337616, 21.015183348860532}'
);

INSERT INTO statuses
	( transportID,state, begginingOfState, endOfState, duration, remaining, eta, coordinates)
VALUES (
	2, 'Waiting for dispatch', now(), now(), '0 days 17 hrs 0 mins', 1234, 'Unknown', '{52.254717669337616, 21.015183348860532}'
);


CREATE TABLE IF NOT EXISTS transports (
    _id serial PRIMARY KEY,
    name varchar ( 200 ) NOT NULL,
    from_ varchar ( 100 ) NOT NULL,
    to_ varchar ( 100 ) NOT NULL,
    drivers integer[] NOT NULL,
    cargo integer NOT NULL,
    total integer,
    state varchar ( 100 ) NOT NULL,
	addedBy INTEGER REFERENCES admins(_id),
    added TIMESTAMP NOT NULL,
    lastModified TIMESTAMP NOT NULL,
    modifiedBy INTEGER REFERENCES admins(_id)
);

INSERT INTO transports
	( name, from_, to_, drivers, cargo, total, state, addedby, added, lastmodified, modifiedby)
VALUES (
	'Cars', 'UK, London', 'Poland, Warsaw',
	'{2 , 1}', 1, 1234, 'In progress', 1, now(), now(), 1
);

INSERT INTO transports
	( name, from_, to_, drivers, cargo, total, state, addedby, added, lastmodified, modifiedby)
VALUES (
	'Chocolate bars for babushka', 'UK, London', 'Poland, Warsaw',
	'{0 , 1}', 3, 1234, 'In progress', 1, now(), now(), 1
);


