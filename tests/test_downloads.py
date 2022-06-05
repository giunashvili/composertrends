from app.database.query import find_all_packages


def test_package_details_has_downloads_property(download_factory, package_factory, client, application):
    package_factory.create()
    download_factory.create()
    download_factory.create()
    download_factory.create()

    with application.app_context():
        package, = find_all_packages()
        vendor, name = [package['vendor'], package['name']]
        data = client.get('/api/package/' + vendor + '/' + name).json

        assert 'downloads' in data
        assert len(data['downloads']) > 0


def test_downloads_record_has_right_structure(package_factory, download_factory, application, client):
    package_factory.create()
    download_factory.create()
    download_factory.create()
    download_factory.create()

    with application.app_context():
        package, = find_all_packages()
        vendor, name = [package['vendor'], package['name']]
        data = client.get('/api/package/' + vendor + '/' + name).json
        download_record, *_ = data['downloads']

        assert 'date' in download_record
        assert 'value' in download_record


def test_package_has_all_the_downloads(package_factory, download_factory, application,client):
    package_factory.create()
    download_factory.create()
    download_factory.create()
    download_factory.create()

    with application.app_context():
        package, = find_all_packages()
        vendor, name = [package['vendor'], package['name']]
        data = client.get('/api/package/' + vendor + '/' + name).json
        download_count = len(data['downloads'])

        assert download_count == 3
