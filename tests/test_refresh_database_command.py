from random import randint
from app.database.query import find_all_downloads, find_all_packages


def test_database_is_cleaned_up_after_refreshing(runner, package_factory, download_factory, application):
    [package_factory.create() for _ in range(randint(1, 5))]
    [download_factory.create() for _ in range(randint(1, 10))]

    with application.app_context():
        packages = find_all_packages()
        downloads = find_all_downloads()

        assert len(packages) > 0
        assert len(downloads) > 0

        runner.invoke(args='db:refresh')

        packages = find_all_packages()
        downloads = find_all_downloads()

        assert len(packages) == 0
        assert len(downloads) == 0
