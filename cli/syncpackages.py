import click
import services
import operator
import threading
from database import query
from flask.cli import with_appcontext

all_packages_count = 0
fetched_packages_count = 0
pretty_packages = []


def fetch_package_detailed_info(packages):
    global fetched_packages_count, all_packages_count, pretty_packages
    for package in packages:
        fetched_packages_count += 1
        print(f'{fetched_packages_count}/{all_packages_count}')
        pretty_package = services.fetch_package_details(package)
        pretty_packages.append(pretty_package)


@click.command('insert:packages')
@with_appcontext
def insert_packages_into_database():
    global pretty_packages, all_packages_count
    raw_packages = services.fetch_all_packages()

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

    last_thread = threading.Thread(
        target=fetch_package_detailed_info,
        args=(raw_packages[package_per_thread * thread_count:],)
    )

    last_thread.start()
    [t.join() for t in threads]
    last_thread.join()

    packages_to_insert = []
    for package in pretty_packages:
        p = (
            package['vendor'],
            package['name'],
            package['description'] or False,
            package['github_stars'] or False,
            package['repository']
        )
        packages_to_insert.append(p)

    query.insert_packages(packages_to_insert)

    click.echo("=========================")
    click.echo("All the packages inserted!")


@click.command('fetch:downloads')
@with_appcontext
def fetch_downloads():
    raw_packages = query.find_all_packages()
    parsed_packages = map(lambda p: p['vendor'] + '/' + p['name'], raw_packages)

    stats = []
    threads = []
    thread_count = 10
    packages_length = len(parsed_packages)
    downloads_per_thread = packages_length // thread_count
    for package in parsed_packages:
        threading.Thread(target=services.fetch_downloads, args=(package,))

    stats = [services.fetch_downloads(package) for package in parsed_packages]

    for stat in stats:
        package, statistics = operator.itemgetter('package', 'stats')(stat)
        vendor, name = package.split('/')
        package = query.find_package(vendor, name)
        query.delete_package_downloads(package['id'])

        downloads_to_insert = [(package['id'], stat['date'], stat['value']) for stat in statistics]
        query.insert_downloads(downloads_to_insert)
    return stats
