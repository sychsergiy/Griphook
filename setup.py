from setuptools import find_packages, setup

NAME = 'griphook'
DESCRIPTION = 'Server monitoring and billing service'
URL = 'http://git.interns.evo/EVO2018-Vlad-team/Griphook/'
AUTHOR = 'Vlad Team'
REQUIRED_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

REQUIRED_PACKAGES = [
    'requests', 'celery', 'sqlalchemy', 'trafaret', 'mypy', 'pytest',
    'alembic', 'pyaml', 'psycopg2', 'flake8'
]

setup(
    name=NAME,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRED_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.6',
    ]
)
