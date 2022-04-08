GET_CARGOS = "SELECT cargos._id, cargos.name, weight, weightUnit, quantity, " \
        "quantityUnit, info, who_added.name as addedBy, cargos.added,  " \
        "lastModified, who_mod.name as modifiedBy FROM cargos " \
        "JOIN admins as who_added ON cargos.addedBy = who_added._id " \
        "JOIN admins as who_mod ON cargos.modifiedBy = who_mod._id;"


GET_DRIVERS = "SELECT drivers._id, firstname, lastname, who_added.name as addedby, added, " \
        "lastmodified, phone, email, who_mod.name as modifiedby FROM drivers " \
        "JOIN admins AS who_added ON drivers.addedBy = who_added._id " \
        "JOIN admins AS who_mod ON drivers.modifiedBy = who_mod._id;"


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
        ":fname, :lname, :ph, :email, :uid, now(), now(), :uid "\
        ");"
