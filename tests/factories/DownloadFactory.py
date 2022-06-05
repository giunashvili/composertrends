from flask import Flask
from random import randint
from app.database.query import insert_download, find_all_packages
from faker import Faker
from tests.factories.PackageFactory import PackageFactory


class DownloadFactory:
    def __init__(self, app: Flask):
        self.app = app
        self.package_factory = PackageFactory(app)

    def create(self, **kwargs):
        with self.app.app_context():
            all_packages = find_all_packages()
            packages_count = len(all_packages)

            if len(all_packages) == 0:
                self.package_factory.create()
                all_packages = find_all_packages()
                packages_count = len(all_packages)

            rand_package_idx = randint(0, packages_count - 1)
            rand_package = all_packages[rand_package_idx]

            fake = Faker()
            insert_download(
                package_id=kwargs.get('package_id', rand_package['id']),
                date=kwargs.get('date', fake.date()),
                value=kwargs.get('value', fake.random_number()),
            )
