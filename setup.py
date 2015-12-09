from setuptools import find_packages, setup
from os.path import expanduser
from glob import glob

setup(
	# Application name:
	name="EasyI3Status",

	# Version number (initial):
	version="0.0.9",

	# Application author details:
	author="Ahmet Emre Cepoglu",
	author_email="aecepoglu@fastmail.fm",

	# Packages
	packages=["easyi3status"],

	# Include additional files into the package
	include_package_data=True,

	# Details
	url="https://bitbucket.org/aecepoglu/easyi3status",

	#
	# license="LICENSE.txt",
	description="Easy status bar for i3 window manager.",

	long_description=open("README.md").read(),

	# Dependent packages (distributions)
	install_requires=[
		"ConfigParser"
	],
	entry_points={
		'console_scripts': [
			'easyi3status = easyi3status:run',
		]
	},
	data_files=[
		(expanduser("~/.easyi3status/modules"), glob("easyi3status/modules/*")),
		(expanduser("~/.easyi3status"), ['easyi3status/config.cfg'])
	],
)
