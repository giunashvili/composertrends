import click
from app import services
import operator
import threading
from app.database import query
from flask.cli import with_appcontext

all_packages_count = 0
fetched_packages_count = 0
pretty_packages = []
package_downloads = []


def fetch_package_detailed_info(packages):
    global fetched_packages_count, all_packages_count, pretty_packages
    for package in packages:
        fetched_packages_count += 1
        print(f'{fetched_packages_count}/{all_packages_count}')
        pretty_package = services.fetch_package_details(package)
        pretty_packages.append(pretty_package)


def fetch_package_downloads(packages):
    global fetched_packages_count, all_packages_count, pretty_packages
    for package in packages:
        fetched_packages_count += 1
        print(f'{fetched_packages_count}/{all_packages_count}')
        pretty_downloads = services.fetch_downloads(package)
        package_downloads.append(pretty_downloads)


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
        end_count = start_count + package_per_thread

        thread = threading.Thread(
            target=fetch_package_detailed_info,
            args=(raw_packages[start_count:end_count],)
        )

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
    global package_downloads, all_packages_count
    raw_packages = query.find_all_packages()
    all_packages_count = len(raw_packages)
    parsed_packages = list(map(lambda p: p['vendor'] + '/' + p['name'], raw_packages))

    threads = []
    thread_count = 10
    downloads_per_thread = all_packages_count // thread_count
    for i in range(thread_count):
        start_count = i * downloads_per_thread
        end_count = start_count + downloads_per_thread

        thread = threading.Thread(
            target=fetch_package_downloads,
            args=(parsed_packages[start_count:end_count],)
        )
        thread.start()
        threads.append(thread)

    last_thread = threading.Thread(
        target=fetch_package_downloads,
        args=(parsed_packages[thread_count * downloads_per_thread:],)
    )
    last_thread.start()

    [thread.join() for thread in threads]
    last_thread.join()

    for download in package_downloads:
        package, statistics = operator.itemgetter('package', 'stats')(download)
        vendor, name = package.split('/')
        package = query.find_package(vendor, name)
        query.delete_package_downloads(package['id'])

        downloads_to_insert = [(package['id'], stat['date'], stat['value']) for stat in statistics]
        query.insert_downloads(downloads_to_insert)
    click.echo('========================')
    click.echo('Package download statistics has been fetched!')
