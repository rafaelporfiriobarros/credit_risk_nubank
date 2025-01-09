from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    esta função retornará a lista de requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements






setup(
name='credit_risk_nubank',
version='0.0.1',
author='Rafael Porfirio',
author_email='rafaporfirio.barros@gmail.com',
packages=find_packages(where='src'),
package_dir={'':'src'},
install_requires=get_requirements('requirements.txt')

)

