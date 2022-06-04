def test_package_response_is_ok(client):
    response = client.get('/api/packages')
    assert response.status_code == 200


def test_package_response_has_right_number_of_records(client, package_factory):
    package_factory.create()
    package_factory.create()
    package_factory.create()

    data = client.get('/api/packages').json
    assert len(data) == 3


def test_package_details_has_all_the_data(client, package_factory):
    package_factory.create()
    package_factory.create()
    package_factory.create()

    data = client.get('/api/packages').json
    record = data[0]

    assert len(data) > 0
    assert 'name' in record
    assert 'vendor' in record
    assert 'description' in record
    assert 'github_stars' in record
    assert 'repository' in record


def test_package_details_route_is_ok(client, package_factory):
    package_factory.create(vendor='redberry', name='spear')
    response = client.get('/api/package/redberry/spear')
    assert response.status_code == 200


def test_non_existing_package_details_route_gives_us_404_error(client):
    response = client.get('/api/package/redberry/arch')
    assert response.status_code == 404
