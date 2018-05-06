from setuptools import setup, find_packages

setup(
    name='battle-city-ai',
    version='0.1',
    description='whatever',
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=['pygame'],
    include_package_data=True,
    extras_require={
        'test': ['pytest'],
    },
)
