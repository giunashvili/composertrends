import operator

from flask import Flask, jsonify
from database.connection import close_db, get_db
from cli.syncpackages import insert_packages_into_database, fetch_downloads
from cli.database import refresh_database

app = Flask(__name__)

# add cli commands
app.cli.add_command(refresh_database)
app.cli.add_command(insert_packages_into_database)
app.cli.add_command(fetch_downloads)

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


@app.route('/package/<path:package>')
def get_package_details(package):
    vendor, name = package.split('/')
    db = get_db()
    fetched_package = db.cursor().execute('SELECT * FROM packages WHERE vendor = ? AND name = ?',
                                          (vendor, name)).fetchone()
    _id, github_stars, description, repo = operator.itemgetter('id', 'github_stars', 'description', 'repository')(fetched_package)
    raw_downloads = db.cursor().execute('SELECT * FROM downloads WHERE package_id = ?', [_id]).fetchall()
    # downloads = [{'date': download['date'], 'value': download['value']} for download in raw_downloads]
    data = {
        'name': name,
        'vendor': vendor,
        'description': description,
        'github_stars': github_stars,
        'repository': repo,
        # 'statistics': downloads,
    }

    return jsonify(data)
