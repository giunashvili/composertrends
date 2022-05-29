import operator
import requests
import json
from database.connection import get_db
import click
from flask.cli import with_appcontext
import threading

all_packages_count = 0
fetched_packages_count = 0
pretty_packages = []


def get_all_packages():
    data = requests.get('https://packagist.org/packages/list.json?vendor=laravel').content
    parsed_data = json.loads(data)
    return parsed_data['packageNames']


def fetch_package_detailed_info(packages):
    global fetched_packages_count, all_packages_count, pretty_packages
    for package in packages:
        fetched_packages_count += 1
        print(f'{fetched_packages_count}/{all_packages_count}')

        package_info = requests.get('https://packagist.org/packages/' + package + '.json').content
        parsed_package_info = json.loads(package_info)['package']

        vendor, name = parsed_package_info['name'].split('/')

        pretty_package = {
            "vendor": vendor,
            "name": name,
            'description': parsed_package_info['description'],
            "repository": parsed_package_info['repository'],
            "github_stars": parsed_package_info['github_stars'],
        }

        pretty_packages.append(pretty_package)


@click.command('insert:packages')
@with_appcontext
def insert_packages_into_database():
    global pretty_packages, all_packages_count
    raw_packages = get_all_packages()
    all_packages_count = len(raw_packages)
    thread_count = 10
    package_per_thread = all_packages_count // thread_count
    threads = []
    for i in range(thread_count):
        start_count = i * package_per_thread
        end_count = (i + 1) * package_per_thread
        thread = threading.Thread(target=fetch_package_detailed_info, args=(raw_packages[start_count:end_count],))
        thread.start()
        threads.append(thread)
    last_thread = threading.Thread(target=fetch_package_detailed_info,
                                   args=(raw_packages[package_per_thread * thread_count:],))
    last_thread.start()
    [t.join() for t in threads]
    last_thread.join()

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


@click.command('fetch:downloads')
@with_appcontext
def fetch_downloads():
    db = get_db()
    raw_packages = db.cursor().execute('SELECT vendor, name FROM packages').fetchall()
    parsed_packages = map(lambda package: package['vendor'] + '/' + package['name'], raw_packages)

    stats = []
    threads = []
    thread_count = 10
    packages_length = len(parsed_packages)
    downloads_per_thread = packages_length // thread_count
    for package in parsed_packages:
        threading.Thread(target=retrieve_downloads, args=(package,))

    stats = [retrieve_downloads(package) for package in parsed_packages]

    for stat in stats:
        package, statistics = operator.itemgetter('package', 'stats')(stat)
        vendor, name = package.split('/')
        package = db.cursor().execute('SELECT id FROM packages where vendor = ? AND name = ?',
                                      (vendor, name)).fetchone()
        db.cursor().execute('DELETE FROM downloads WHERE package_id = ?', (package['id'],))
        db.commit()

        statistics_to_insert = [(package['id'], stat['date'], stat['value']) for stat in statistics]
        db.cursor().executemany('INSERT INTO downloads (package_id, date, value) VALUES (?, ?, ?)',
                                statistics_to_insert)
    return stats
