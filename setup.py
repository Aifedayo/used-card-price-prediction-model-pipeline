import os
from setuptools import find_packages, setup #type: ignore
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filepath:str)->List[str]:
    """
    This func will read the requirements.txt file
    and append it to a list
    """
    with open('requirements.txt') as file:
        requirements = file.readlines()
        requirements = [req.replace('/n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='used-car-price-prediction-model',
    version='0.0.1',
    author='Akeem I. Lagundoye',
    author_email='akeemifedayolag@gmail.com',
    requires=get_requirements('requirements.txt'),
    packages=find_packages(),
)
