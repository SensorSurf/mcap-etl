import os

from setuptools import setup, find_packages


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='mcap-etl',
    author='SensorSurf',
    author_email='support@sensorsurf.com',
    description='Transform mcap (or rosbag) files into databases or other files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SensorSurf/mcap-etl',
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
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
    keywords='ros, ros2, rosbag, mcap, timescale, etl, timeseries, database, etl',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mcap-etl=mcap_etl.main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/SensorSurf/mcap-etl/issues',
        'Source': 'https://github.com/SensorSurf/mcap-etl',
    },
)
