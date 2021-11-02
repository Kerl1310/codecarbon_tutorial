from setuptools import setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRED = f.read().splitlines()

setup(name='CodeCarbonTutorial',
      version='1.0',
      description='Tutorial using CodeCarbon',
    #   long_description=open('README.md').read(),
      author='Kyle Jones',
      author_email='kylejones1310@outlook.com',
      url='',
      packages=find_packages(exclude=('tests', 'tests.integration',)),
      keywords='python cloudwatch codecarbon',
      python_requires=">=3.6",
      install_requires=INSTALL_REQUIRED,
     )