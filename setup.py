from setuptools import find_packages, setup
from typing import List
def requirements_install(requirements_file:str)->List[str]:
    """
    Reads a requirements file and returns a list of requirements.

    Args:
        requirements_file (str): Path to the requirements file.

    Returns:
        List[str]: A list of requirements.
    """
    with open(requirements_file,'r') as f:
        requirements=f.read().split('\n')
        if '-e .' in requirements:
            requirements.remove('-e .')
        return requirements

setup(
    name = 'isd',
    version= '0.0.0',
    author= 'santhosh',
    author_email= 'borasanthosh921@gmail.com',
    packages= find_packages(),
    install_requires = requirements_install('requirements.txt')
)