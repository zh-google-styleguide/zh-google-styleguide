Manually generate PDF documents
-------

# Debian 9

```shell
sudo apt install texlive-lang-chinese texlive-lang-cjk texlive-xetex \
latexmk texlive-latex-extra texlive-latex-recommended python-pip \
texlive-latex-base texlive-plain-extra texlive-fonts-recommended \
texlive-generic-recommended
```

# Python pip

```shell
sudo pip install Sphinx commonmark sphinx-rtd-theme
```

if download is too slow, try use local mirror

```shell
sudo pip Sphinx commonmark sphinx-rtd-theme -i https://mirrors.aliyun.com/pypi/simple/
```

# Generate PDF

```shell
make latex
make latexpdf
```

# Q & A

1. If occuring XXX file missing

use follow url relace REPLACE-MISSING-FILE-NAME to you want find and install missing package

https://packages.debian.org/search?searchon=contents&keywords=RELACE-MISSING-FILE-NAME&mode=path&suite=oldstable&arch=any


