from setuptools import setup, find_packages

setup(
    name='mgski',
    version='0.0.2',
    license='MIT',
    author="Mayank Gupta",
    author_email='seekmayank@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mgski project',
    install_requires=[
          'wheel',
      ]
)
