import pathlib

from setuptools import find_packages, setup

from alcss.__init__ import __version__

with open("readme.md", encoding = "utf-8") as f:
	description = f.read()

setup(
		name                          = 'alcss',
		version                       = __version__,
		packages                      = find_packages(),
		author                        = 'Miasnenko Dmitry',
		author_email                  = 'clowzed.work@gmail.com',
		url                           = 'https://github.com/clowzed/alcss.git',
		long_description              = description,
        long_description_content_type = 'text/markdown',
		install_requires              = ['argparse'],
		entry_points = 
		{
			'console_scripts': [
				'alcss = alcss.run:main'
		]
		}
)
