from setuptools import find_packages, setup
setup(
    name='anupam-anand-eaton-library-0.1',
    package_dir={"": "clients"},
    packages=find_packages(where='clients'),
    version='0.1.0',
    description='Python library',
    author='Anupam Anand',
    license='Eaton',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.0.1'],
    test_suite='tests',
)