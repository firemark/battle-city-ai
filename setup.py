from setuptools import setup, find_packages

setup(
    name='battle-city-ai',
    version='0.1',
    description='whatever',
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=[
        'pygame==1.9.4',
    ],
    include_package_data=True,
    extras_require={
        'test': [
            'pytest==3.6.3',
            'pytest-asyncio==0.9.0',
            'pytest-cov==2.5.1',
            'asynctest==0.12.2',
            'coverage==4.5.1', 
        ],
    },
)
