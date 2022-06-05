import json
import responses
from app.database.query import find_all_packages, find_package


@responses.activate
def test_insert_packages_cli_command(runner, application):
    all_packages_response_data = {
        'packageNames': [
            'redberry/spear',
            'spatie/laravel-translatable',
            'pestphp/pest',
        ]
    }

    package_details_response_data = [
        {
            'package': {
                'name': 'redberry/spear',
                'description': 'Redberry spear - run any language in Laravel!',
                'repository': 'https://github.com/RedberryProducts/Spear',
                'github_stars': 7,
            }
        },
        {
            'package': {
                'name': 'spatie/laravel-translatable',
                'description': 'A trait to make an Eloquent model hold translations',
                'repository': 'https://github.com/spatie/laravel-translatable',
                'github_stars': 1700,
            }
        },
        {
        'package': {
                'name': 'pestphp/pest',
                'description': 'An elegant PHP Testing Framework.',
                'repository': 'https://github.com/pestphp/pest',
                'github_stars': 4800,
            }
        }
    ]

    responses.add(
        url='https://packagist.org/packages/list.json?vendor=laravel',
        body=json.dumps(all_packages_response_data),
        headers={
            'Content-Type': 'application/json'
        },
        method=responses.GET
    )

    for package_detailed_response in package_details_response_data:
        responses.add(
            url=f'https://packagist.org/packages/{package_detailed_response["package"]["name"]}.json',
            body=json.dumps(package_detailed_response),
            headers={
                'Content-Type': 'application/json'
            },
            method=responses.GET
        )

    result = runner.invoke(args='insert:packages')

    with application.app_context():
        packages_in_database = find_all_packages()

        redberry_spear_in_database = find_package('redberry', 'spear')

        assert result.exit_code == 0
        assert "All the packages inserted!" in result.output
        assert len(packages_in_database) == 3
        assert redberry_spear_in_database is not None

