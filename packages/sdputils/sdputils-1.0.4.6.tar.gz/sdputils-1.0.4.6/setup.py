import setuptools

setuptools.setup(
    name="sdputils",
    version="1.0.4.6",
    author="Lucas S. Maximiano",
    description="Utils' functions to use inside the Semantix Data Platform for data transformation.",
    install_requires=[
          'pandas==1.2.4',
          'sqlalchemy==1.4.9',
          'pyhive==0.6.5',
          'unidecode==1.3.3'
      ],
    py_modules=['sdputils'],
    packages=setuptools.find_packages('.')
)