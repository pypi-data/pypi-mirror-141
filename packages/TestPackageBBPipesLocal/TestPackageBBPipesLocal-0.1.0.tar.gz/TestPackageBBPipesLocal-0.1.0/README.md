# Bitbucket Pipelines Pipe: PyPI publish

This pipe can publish your python package to [PyPI](https://pypi.org).

The Python Package Index (PyPI) is a repository of software for the Python programming language.
PyPI helps you find and install software developed and shared by the Python community. [Learn about installing packages](https://packaging.python.org/tutorials/installing-packages/).

Package authors use PyPI to distribute their software. [Learn how to package your Python code for PyPI](https://packaging.python.org/distributing/).

## YAML Definition

Add the following snippet to the script section of your `bitbucket-pipelines.yml` file:

```yaml
- pipe: atlassian/pypi-publish:0.3.1
  variables:
    PYPI_USERNAME: '<string>'
    PYPI_PASSWORD: '<string>'
    # REPOSITORY: '<string>' # Optional.
    # DISTRIBUTIONS: '<string>' # Optional.
    # FOLDER: '<string>' # Optional.
    # DEBUG: '<boolean>' # Optional.
```
## Variables

| Variable              | Usage                                                       |
| --------------------- | ----------------------------------------------------------- |
| PYPI_USERNAME (*)     | PyPI account user name                                      |
| PYPI_PASSWORD (*)     | PyPI account password                                       |
| REPOSITORY            | PyPI repository url. Default `https://upload.pypi.org/legacy/`               |
| DISTRIBUTIONS         | List of white space separated distributions to publish. Default `sdist`           |
| FOLDER                | Folder containing the setup.py script. Default is current working directory |
| DEBUG                 | Turn on extra debug information. Default: `false`. |

_(*) = required variable._

## Prerequisites

PyPI username and password are necessary to use this pipe.

- To register click [here](https://pypi.org/account/register/).
- Add password `PYPI_PASSWORD` as [secured environment variable](https://confluence.atlassian.com/x/0CVbLw#Environmentvariables-Securedvariables) in Bitbucket Pipelines.


## Examples

Basic example:

```yaml
script:
  - pipe: atlassian/pypi-publish:0.3.1
    variables:
      PYPI_USERNAME: $PYPI_USERNAME
      PYPI_PASSWORD: $PYPI_PASSWORD
```

Advanced example:

```yaml
script:
  - pipe: atlassian/pypi-publish:0.3.1
    variables:
      variables:
      PYPI_USERNAME: $PYPI_USERNAME
      PYPI_PASSWORD: $PYPI_PASSWORD
      DISTRIBUTIONS: 'bdist_wheel'
      REPOSITORY: 'https://test.pypi.org/legacy/'
      FOLDER: 'myfolder'

```

## Support
If you’d like help with this pipe, or you have an issue or feature request, [let us know on Community][community].

If you’re reporting an issue, please include:

- the version of the pipe
- relevant logs and error messages
- steps to reproduce


[community]: https://community.atlassian.com/t5/forums/postpage/board-id/bitbucket-pipelines-questions?add-tags=pipes,python,pypi,publish
