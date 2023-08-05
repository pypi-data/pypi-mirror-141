from setuptools import setup, find_packages

setup(name='openkit',
      version='1.0.1',
      packages=find_packages(),
      package_data={'openkit': ['wrappers/*']},
      install_requires=[],
      author='David Lopes',
      author_email='davidribeirolopes@gmail.com',
      description='Dynatrace OpenKit implementation in Python',
      long_description='The Dynatrace OpenKit implementation in Python',
      url='https://github.com/dlopes7/openkit-python',
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"]
      )
