# -*- coding: utf-8 -*-



import sys, os
project = u'Google 开源项目风格指南'
copyright = u''
version = u''
release = u''

source_suffix = '.rst'
master_doc = 'contents'
language = 'en_US'
exclude_patterns = ['_build']
extensions = ['sphinx.ext.pngmath']
pygments_style = 'sphinx'

# on_rtd is whether we are on readthedocs.org
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# otherwise, readthedocs.org uses their theme by default, so no need to specify it

html_title = u'Google 开源项目风格指南'
htmlhelp_basename = 'google-styleguide'
html_add_permalinks = None

file_insertion_enabled = False
latex_documents = [
  ('index', 'google-styleguide.tex', u'Google 开源项目风格指南',
   u'', 'manual'),
]


#Add sponsorship and project information to the template context.
context = {
    'MEDIA_URL': "/media/",
    'slug': 'google-styleguide',
    'name': u'Google 开源项目风格指南',
    'analytics_code': 'None',
}

html_context = context
