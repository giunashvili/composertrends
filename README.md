### ComposerTrends

<a href="https://composertrends.com" target="_blank">composertrends.com</a> is a platform to visit and find a suitable composer package for your next-big-idea project.
ComposerTrends is inspired by a beautiful platform [npmtrends.com](https://npmtrends.com)

#### Table of Contents

* [Requirements](#requirements)
* [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)
* [Resources](#resources)


#### Requirements

* [Python 3.8](https://www.python.org/)

#### Tech Stack
* [Flask v2.1.2](https://flask.palletsprojects.com/en/2.1.x/)
* [requests v2.27.1](https://requests.readthedocs.io/en/latest/)
* [Jinja2 v3.1.2](https://jinja.palletsprojects.com/en/3.1.x/)
* [Faker v13.12.0](https://faker.readthedocs.io/en/master/)
* [Pytest v7.1.2](https://docs.pytest.org/en/7.1.x/)
* [Responses v0.21.0](https://github.com/getsentry/responses)
* [Gunicorn v20.0.1](https://docs.gunicorn.org/en/stable/)

#### Getting Started
In order to get started with the project clone the github repo:
```commandline
git clone git@github.com:giunashvili/composertrends.git
```

go inside the project:
```commandline
cd composertrends
```

install the dependencies:
```commandline
pip install -r requirements.txt
```

now we can activate virtual environment:
```commandline
source ./venv/bin/activate
```

export several environment variables for Flask to be able to find our application and set appliaction mode:
```commandline
export FLASK_APP=server
export FLASK_ENV=development
```

and now we should be able to run our application:
```commandline
flask run
```


#### Resources
comming soon...