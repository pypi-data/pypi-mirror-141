# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as file:
    readme = file.read()

with open('LICENSE') as file:
    license = file.read()
    
setup(
  name = 'ROSSpy',      
  package_dir = {'core':'rosspy'},
  packages = find_packages(),
  package_data = {
	'rosspy':['water_bodies/*','databases/*','processed_databases/*', 'test/*', 'test/*/*'],
  },
  version = '0.0.20',
  license = license,
  description = "Software for predicting the brine and scaling consequences of RO desalination.", 
  long_description = readme,
  author = 'Andrew Freiburger',               
  author_email = 'andrewfreiburger@gmail.com',
  url = 'https://github.com/freiburgermsu/ROSS',   
  keywords = ['desalination', 'reactive transport', 'geochemistry', 'sustainability', 'civil engineering', 'fluid mechanics'],
  install_requires = ['matplotlib', 'chemicals', 'chempy', 'scipy', 'chemw', 'pubchempy', 'pandas', 'phreeqpy', 'sigfig']
)