from flask import Flask, jsonify
from database.connection import close_db, get_db
from cli.syncpackages import insert_packages_into_database, fetch_downloads
from cli.database import refresh_database
from database.query import find_package, find_all_packages, find_package_downloads

app = Flask(__name__)

app.cli.add_command(refresh_database)
app.cli.add_command(insert_packages_into_database)
app.cli.add_command(fetch_downloads)

app.teardown_appcontext(close_db)


@app.route('/packages')
def packages():
    fetched_packages = find_all_packages()

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
    fetched_package = find_package(vendor, name)
    raw_downloads = find_package_downloads(fetched_package['id'])
    downloads = [{'date': download['date'], 'value': download['value']} for download in raw_downloads]
    data = {
        'name': fetched_package['name'],
        'vendor': fetched_package['vendor'],
        'description': fetched_package['description'],
        'github_stars': fetched_package['github_stars'],
        'repository': fetched_package['repo'],
        'statistics': downloads,
    }

    return jsonify(data)
