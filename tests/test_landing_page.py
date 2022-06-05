def test_landing_page_is_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_landing_page_includes_composertrends_keyword(client):
    response = client.get('/')
    content = response.data.lower()
    assert b'composertrends' in content
