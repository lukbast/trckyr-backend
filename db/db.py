import databases
from os import getenv


def create_db_url(host: str, port: str, db_name: str, user: str,
                  password: str):
    return 'postgresql://{}:{}@{}:{}/{}'.format(
        user, password, host, port, db_name)


DB_URL = create_db_url(getenv("POSTGRES_URL"),
                       getenv("PORT"),
                       getenv("POSTGRES_DB"),
                       getenv("POSTGRES_USER"),
                       getenv("POSTGRES_PASSWORD"))

db_conn = databases.Database(DB_URL)

GET_CARGOS = "SELECT cargos._id, cargos.name, weight, weightUnit, quantity, " \
             "quantityUnit, info, who_added.name as addedBy, cargos.added,  " \
             "lastModified, who_mod.name as modifiedBy FROM cargos " \
             "JOIN admins as who_added ON cargos.addedBy = who_added._id " \
             "JOIN admins as who_mod ON cargos.modifiedBy = who_mod._id ORDER BY cargos._id;"

GET_DRIVERS = "SELECT drivers._id, firstname, lastname, who_added.name as addedby, added, " \
              "lastmodified, phone, email, who_mod.name as modifiedby FROM drivers " \
              "JOIN admins AS who_added ON drivers.addedBy = who_added._id " \
              "JOIN admins AS who_mod ON drivers.modifiedBy = who_mod._id ORDER BY drivers._id;"

GET_TRANSPORTS = "SELECT t._id, t.name, from_, to_, drivers, cargo, " \
                 "total, t.state, who_added.name as addedby, added, lastmodified, who_mod.name as modifiedby " \
                 "FROM transports as t " \
                 "JOIN admins AS who_added ON t.addedBy = who_added._id " \
                 "JOIN admins AS who_mod ON t.modifiedBy = who_mod._id;"

NEW_CARGO = "INSERT INTO cargos " \
            "(name, weight, weightUnit, quantity, quantityUnit, info, addedBy, " \
            "added, lastModified, modifiedBy ) " \
            "VALUES ( " \
            ":name, :wth, :wunit, :qty , :qunit, :info, :uid, now(), now(), :uid " \
            ");"

NEW_DRIVER = "INSERT INTO drivers " \
             "(firstname, lastname, phone, email, addedBy, added, lastModified, modifiedBy) " \
             "VALUES ( " \
             ":fname, :lname, :ph, :email, :uid, now(), now(), :uid " \
             ");"
UPDATE_CARGO = "UPDATE cargos SET name=:name, weight=:w, weightunit=:wunit, " \
               "quantity=:q, quantityunit=:qunit, info=:info, lastmodified=now(), " \
               "modifiedby=:uid  WHERE _id = :id;"
UPDATE_DRIVERS = "UPDATE drivers SET firstname=:fname, lastname=:lname, " \
                 "phone=:ph, email=:email, lastmodified= now(), modifiedby= :uid WHERE _id = :id;"

NEW_TRANSPORT = "INSERT INTO transports" \
                "( name, from_, to_, drivers, cargo, total, state, addedby, added, lastmodified, modifiedby) " \
                "VALUES ( :name, :from, :to, :drivers, :cargo, :total, " \
                "'Waiting for dispatch', :uid, now(), now(), :uid " \
                "); "

INITIAL_STATUS = "INSERT INTO statuses " \
                 "( transportID, state, begginingOfState, endOfState, duration, remaining, eta, coordinates) " \
                 "VALUES ( :id, 'Waiting for dispatch', now(), null, null, :rem_dist, " \
                 ":eta, :from_coors );"
