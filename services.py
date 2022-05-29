import requests
import json
from typing import Dict, List


def fetch_all_packages() -> List:
    data = requests.get('https://packagist.org/packages/list.json?vendor=laravel').content
    parsed_data = json.loads(data)
    return parsed_data['packageNames']


def fetch_downloads(package) -> Dict:
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


def fetch_package_details(package) -> Dict:
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
    return pretty_package
