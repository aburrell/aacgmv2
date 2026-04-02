"""Configuration file for documetation."""
from pyproject_parser import PyProject

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.ifconfig',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon',
              'numpydoc']

# General information about the project.
info = PyProject.load("../pyproject.toml")

# Set the basic variables
source_suffix = '.rst'
master_doc = 'index'
project = 'AACGM-v2 Python library'
year = '2026'
author = 'Angeline G. Burrell, et al.'
copyright = '{0}, {1}'.format(year, author)
version = release = info.project['version'].base_version

pygments_style = 'trac'
templates_path = ['.']
html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = True
html_sidebars = {'**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html']}
html_short_title = '%s-%s' % (project, version)

# Set up hyperlinks to not check in unit tests due to 403 errors
linkcheck_ignore = [r'https://scrutinizer-ci.com:\d+/',
                    r'https://zenodo.org:\d+/]
