"""Configuration file for documetation."""
import os
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
year = '2024'
author = 'Angeline G. Burrell, et al.'
copyright = '{0}, {1}'.format(year, author)
version = release = info.project['version'].base_version

# `on_rtd` is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# Only import and set the theme if we're building docs locally
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

pygments_style = 'trac'
templates_path = ['.']
html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = True
html_sidebars = {'**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html']}
html_short_title = '%s-%s' % (project, version)
