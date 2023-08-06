import os

from bitbucket_pipes_toolkit.test import PipeTestCase


setup_py_contents = """
from setuptools import setup

setup(
    name = '{package_name}',
    version = '{version}',
    url = 'https://example.com',
    author = 'Atlassian',
    author_email='bitbucketci-team@atlassian.com',
    description = 'Test package',
)
"""

filename = 'setup.py'


def create_setup_py():
    if os.getenv('CI') is not None:
        package_name = 'TestPackageBBPipes'
        version = f'0.{os.getenv("BITBUCKET_BUILD_NUMBER")}'
    else:
        package_name = 'TestPackageBBPipesLocal'
        version = f'0.1.0'
    with open(filename, 'w') as setup_py:
        setup_py.write(setup_py_contents.format(package_name=package_name, version=version))


class PyPITestCase(PipeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_setup_py()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        os.remove(filename)

    def test_no_parameters(self):
        result = self.run_container()
        self.assertRegex(result, "PYPI_PASSWORD:\n- required field")

    def test_sdist(self):
        result = self.run_container(environment={
            'PYPI_USERNAME': os.getenv("PYPI_USERNAME"),
            'PYPI_PASSWORD': os.getenv("PYPI_PASSWORD"),
            'REPOSITORY': 'https://test.pypi.org/legacy/',
            'SKIP_EXISTING': '1',
        })

        self.assertRegex(result, 'Successfully uploaded the package')

    def test_bdist_wheel(self):
        result = self.run_container(environment={
            'PYPI_USERNAME': os.getenv("PYPI_USERNAME"),
            'PYPI_PASSWORD': os.getenv("PYPI_PASSWORD"),
            'REPOSITORY': 'https://test.pypi.org/legacy/',
            'DISTRIBUTIONS': 'bdist_wheel',
            'SKIP_EXISTING': '1',
        })

        self.assertRegex(result, 'Successfully uploaded the package')

    def test_sdist_bdist_wheel(self):
        result = self.run_container(environment={
            'PYPI_USERNAME': os.getenv("PYPI_USERNAME"),
            'PYPI_PASSWORD': os.getenv("PYPI_PASSWORD"),
            'REPOSITORY': 'https://test.pypi.org/legacy/',
            'DISTRIBUTIONS': 'sdist bdist_wheel',
            'SKIP_EXISTING': '1',
        })

        self.assertRegex(result, 'Successfully uploaded the package')

    def test_folder_doesnt_exist(self):
        result = self.run_container(environment={
            'PYPI_USERNAME': os.getenv("PYPI_USERNAME"),
            'PYPI_PASSWORD': os.getenv("PYPI_PASSWORD"),
            'REPOSITORY': 'https://test.pypi.org/legacy/',
            'FOLDER': '/nosuchfolder',
            'SKIP_EXISTING': '1',
        })

        self.assertRegex(result, 'No such file or directory')
