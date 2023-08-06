from setuptools import setup

setup(name='pyghaseel',
      version='0.1',
      description='Simple text cleaning package that supports Arabic and English text',
      install_requires=[
        'regex',
        'numpy',
        'pandas',
        'mysql-connector-python',
        'nltk',
        'tashaphyne',
        'qalsadi',
        'Arabic-Stopwords',
        'pyarabic'
        ],
      url="https://github.com/ATWltd/pyghaseel",
      packages=['pyghaseel'],
      zip_safe=False)
