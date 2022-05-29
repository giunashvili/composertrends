from flask import Flask, jsonify
from database.connection import close_db, get_db
from cli.syncpackages import insert_packages_into_database, fetch_downloads
from cli.database import refresh_database

app = Flask(__name__)

# add cli commands
app.cli.add_command(refresh_database)
app.cli.add_command(insert_packages_into_database)
# app.cli.add_command(fetch_downloads)

app.teardown_appcontext(close_db)


@app.route('/packages')
def packages():
    db = get_db()
    fetched_packages = db.cursor().execute("SELECT * FROM packages").fetchall()

    def prettify(package):
        return {
            'name': package['name'],
            'vendor': package['vendor'],
            'description': package['description'],
            'github_stars': package['github_stars'],
            'repository': package['repository'],
        }

    pretty_packages = list(map(prettify, fetched_packages))
    return jsonify(pretty_packages)


@app.route('/test')
def test():
    return jsonify(fetch_downloads())
