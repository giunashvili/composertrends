from flask import Flask, jsonify, abort
from app.database.connection import close_db
from app.cli.syncpackages import insert_packages_into_database, fetch_downloads
from app.cli.database import refresh_database
from app.database.query import find_package, find_all_packages, find_package_downloads

flask = Flask(__name__)

flask.cli.add_command(refresh_database)
flask.cli.add_command(insert_packages_into_database)
flask.cli.add_command(fetch_downloads)

flask.teardown_appcontext(close_db)


@flask.route('/api/packages')
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


@flask.route('/api/package/<path:package>')
def get_package_details(package):
    vendor, name = package.split('/')
    fetched_package = find_package(vendor, name)

    if fetched_package is None:
        abort(404)

    raw_downloads = find_package_downloads(fetched_package['id'])
    downloads = [{'date': download['date'], 'value': download['value']} for download in raw_downloads]
    data = {
        'name': fetched_package['name'],
        'vendor': fetched_package['vendor'],
        'description': fetched_package['description'],
        'github_stars': fetched_package['github_stars'],
        'repository': fetched_package['repository'],
        'statistics': downloads,
    }

    return jsonify(data)
