import os

from setuptools import setup, find_packages


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mcap_etl',
    version='0.1.1',
    author='SensorSurf',
    author_email='support@sensorsurf.com',
    description='Transform mcap (or rosbag) files into databases or other files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SensorSurf/mcap_etl',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='ros, ros1, rosbag, mcap, timescale, etl, timeseries, database, etl',
    install_requires=[
        'jmespath==1.0.1',
        'lz4==4.3.2',
        'mcap==1.0.2',
        'numpy==1.23.1',
        'pandas==2.0.1',
        'psycopg2-binary==2.9.6',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'rosbags==0.9.15',
        'ruamel.yaml==0.17.26',
        'ruamel.yaml.clib==0.2.7',
        'six==1.16.0',
        'tzdata==2023.3',
        'urllib3==1.26.15',
        'zstandard==0.21.0',
    ],
    entry_points={
        'console_scripts': [
            'mcap_etl=mcap_etl.main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/SensorSurf/mcap_etl/issues',
        'Source': 'https://github.com/SensorSurf/mcap_etl',
    },
)
