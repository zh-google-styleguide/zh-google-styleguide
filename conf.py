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

html_title = u'Google 开源项目风格指南'
html_theme = 'haiku'
html_theme_path = ['../../../templates/sphinx', ]
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
