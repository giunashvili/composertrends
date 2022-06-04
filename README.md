### ComposerTrends


#### Table of Contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)
* [Resources](#resources)


#### Introduction
ComposerTrends will be a platform to visit and find a suitable composer package for your next-big-idea project.
ComposerTrends is inspired by a beautiful platform [npmtrends.com](https://npmtrends.com)

#### Requirements

* [Python 3.8](https://www.python.org/)

#### Tech Stack
* [Flask v2.1.x](https://flask.palletsprojects.com/en/2.1.x/)
* [requests v2.27.x](https://requests.readthedocs.io/en/latest/)
* [Jinja2 v3.1.x](https://jinja.palletsprojects.com/en/3.1.x/)
* [Faker v13.12.x](https://faker.readthedocs.io/en/master/)
* [Pytest v7.1.x](https://docs.pytest.org/en/7.1.x/)

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

now you we can activate virtual environment:
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