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
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:    
    latex_elements = {    
        # The paper size ('letterpaper' or 'a4paper').    
        #'papersize': 'letterpaper',    
        # The font size ('10pt', '11pt' or '12pt').    
        #'pointsize': '10pt',    
        # Additional stuff for the LaTeX preamble.    
        'preamble': r'''    
        \hypersetup{unicode=true}    
        \usepackage{CJKutf8}    
        \DeclareUnicodeCharacter{00A0}{\nobreakspace}    
        \DeclareUnicodeCharacter{2203}{\ensuremath{\exists}}    
        \DeclareUnicodeCharacter{2200}{\ensuremath{\forall}}    
        \DeclareUnicodeCharacter{2286}{\ensuremath{\subseteq}}    
        \DeclareUnicodeCharacter{2713}{x}    
        \DeclareUnicodeCharacter{27FA}{\ensuremath{\Longleftrightarrow}}    
        \DeclareUnicodeCharacter{221A}{\ensuremath{\sqrt{}}}    
        \DeclareUnicodeCharacter{221B}{\ensuremath{\sqrt[3]{}}}    
        \DeclareUnicodeCharacter{2295}{\ensuremath{\oplus}}    
        \DeclareUnicodeCharacter{2297}{\ensuremath{\otimes}}    
        \begin{CJK}{UTF8}{gbsn}    
        \AtEndDocument{\end{CJK}}    ''',    
    }
else:    
    latex_elements = {        
        'papersize' : 'a4paper',        
        'utf8extra' : '',        
        'inputenc'  : '',        
        'babel'     : r'''\usepackage[english]{babel}''',        
        'preamble' : r'''        \usepackage{ctex}        ''',    
    }  
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
