from flask import Flask
from faker import Faker
from app.database.query import insert_package


class PackageFactory:
    def __init__(self, app):
        self.app: Flask = app

    def create(self, **kwargs):
        with self.app.app_context():
            fake = Faker()
            insert_package(
                vendor=kwargs.get('vendor', fake.word()),
                name=kwargs.get('name', fake.word()),
                description=kwargs.get('description', fake.paragraph()),
                github_stars=kwargs.get('github_stars', fake.random_number()),
                repository=kwargs.get('repository', fake.url())
            )
