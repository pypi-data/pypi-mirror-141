from setuptools import find_packages, setup

setup(
    name='pyfrench',
    packages=find_packages(),
    version='0.1.0',
    description='Une librairie qui traduit python en français',
    long_description='Une librairie python de toute versions qui traduit ajoute les même fonctionnalités python sur le module en français.',
    author='Artic#6377',
    author_email="artic.admisoffi@gmail.com",
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)