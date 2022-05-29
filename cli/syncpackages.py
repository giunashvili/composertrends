import requests
import json
from database.connection import get_db
import click
from flask.cli import with_appcontext

all_packages_count = 0
fetched_packages_count = 0


def get_all_packages():
    data = requests.get('https://packagist.org/packages/list.json').content
    parsed_data = json.loads(data)
    global all_packages_count
    end_count = 150
    all_packages_count = len(parsed_data['packageNames'][:end_count])
    return parsed_data['packageNames'][:end_count]


def extract_package_info(package):
    global fetched_packages_count, all_packages_count
    fetched_packages_count += 1
    package_info = requests.get('https://packagist.org/packages/' + package + '.json').content
    parsed_package_info = json.loads(package_info)['package']
    vendor, name = parsed_package_info['name'].split('/')

    print(f'{fetched_packages_count}/{all_packages_count}')
    return {
        "vendor": vendor,
        "name": name,
        'description': parsed_package_info['description'],
        "repository": parsed_package_info['repository'],
        "github_stars": parsed_package_info['github_stars'],
    }


@click.command('insert:packages')
@with_appcontext
def insert_packages_into_database():
    raw_packages = get_all_packages()
    pretty_packages = list(map(extract_package_info, raw_packages))
    packages_to_insert = []
    for package in pretty_packages:
        p = (package['vendor'], package['name'], package['description'] or 'NULL', package['github_stars'] or 'NULL',
             package['repository'])
        packages_to_insert.append(p)

    db = get_db()
    query = "INSERT INTO packages (vendor, name, description, github_stars, repository) VALUES (?, ?, ?, ?, ?)"

    try:
        db.cursor().executemany(query, packages_to_insert)
        db.commit()
    except:
        print(query)

    click.echo("=========================")
    click.echo("All the packages inserted!")


# @click.command('fetch:downloads')
# @with_appcontext
def fetch_downloads():
    db = get_db()
    raw_packages = db.cursor().execute('SELECT vendor, name FROM packages').fetchall()
    parsed_packages = map(lambda package: package['vendor'] + '/' + package['name'], raw_packages)

    def retrieve_downloads(package):
        raw_data = requests.get('https://packagist.org/packages/' + package + '/stats/all.json').content
        parsed_json = json.loads(raw_data)
        is_monthly = parsed_json['average'] == 'monthly'

        result = {
            "package": package,
            "stats": [],
        }
        values = parsed_json['values'][package]
        for i in range(0, len(parsed_json['labels'])):
            label = parsed_json['labels'][i]
            date = label + '-01' if is_monthly else label
            stat = {
                "date": date,
                "value": values[i]
            }
            result['stats'].append(stat)

        return result

    stats = [retrieve_downloads(package) for package in parsed_packages]

    return stats
