from app.database.connection import get_db


def find_package(vendor, name):
    db = get_db()
    sql = 'SELECT * FROM packages where vendor = ? AND name = ?'
    package = db.cursor().execute(sql, [vendor, name]).fetchone()
    return package


def find_all_packages():
    db = get_db()
    sql = 'SELECT * FROM packages'
    return db.cursor().execute(sql).fetchall()


def find_package_downloads(_id):
    db = get_db()
    sql = 'SELECT * FROM downloads WHERE package_id = ?'
    return db.cursor().execute(sql, [_id]).fetchall()


def find_all_downloads():
    db = get_db()
    sql = 'SELECT * FROM downloads'
    return db.cursor().execute(sql).fetchall()


def insert_package(vendor, name, description, github_stars, repository):
    db = get_db()
    sql = "INSERT INTO packages (vendor, name, description, github_stars, repository) VALUES (?, ?, ?, ?, ?)"
    bindings = [vendor, name, description, github_stars, repository]
    db.cursor().execute(sql, bindings)
    db.commit()


def insert_packages(packages):
    db = get_db()
    sql = "INSERT INTO packages (vendor, name, description, github_stars, repository) VALUES (?, ?, ?, ?, ?)"
    db.cursor().executemany(sql, packages)
    db.commit()


def delete_package_downloads(package_id):
    db = get_db()
    sql = 'DELETE FROM downloads WHERE package_id = ?'
    db.cursor().execute(sql, [package_id])
    db.commit()


def insert_downloads(downloads):
    db = get_db()
    sql = 'INSERT INTO downloads (package_id, date, value) VALUES (?, ?, ?)'
    db.cursor().executemany(sql, downloads)


def insert_download(package_id, date, value):
    db = get_db()
    sql = 'INSERT INTO downloads (package_id, date, value) VALUES (?, ?, ?)'
    values = [package_id, date, value]
    db.cursor().execute(sql, values)
    db.commit()
