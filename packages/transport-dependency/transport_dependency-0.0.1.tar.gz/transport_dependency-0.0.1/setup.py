from setuptools import setup
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(ROOT, 'README.md'), encoding="utf-8") as f:
    README = f.read()

setup(name='transport_dependency',
      version='0.0.1',
      description='A package to compute optimal transport based dependency measures such as the transport correlation',
     author='Thomas Giacomo Nies',
      author_email='thomas.nies@uni-goettingen.de',
      long_description_content_type="text/markdown",
      long_description=README,
      license='MIT',
      packages=['transport_dependency'],
      include_package_data=True,
      install_requires=[
          'numpy',
          'scipy',
          'pot'
      ],
      zip_safe=False)
