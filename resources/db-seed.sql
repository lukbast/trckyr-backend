CREATE TABLE IF NOT EXISTS admins (
    _id serial PRIMARY KEY,
	name VARCHAR ( 500 ) NOT NULL,
	password VARCHAR ( 500 ) NOT NULL,
	created TIMESTAMP NOT NULL
);

INSERT INTO admins (name, password, created) VALUES ('TEST ACCOUNT', 'test', now());


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
	addedBy INTEGER REFERENCES admins(_id),
    added TIMESTAMP NOT NULL,
    lastModified TIMESTAMP NOT NULL,
    modifiedBy INTEGER REFERENCES admins(_id)
);