# Manually generate PDF documents
-------

OS: Debian 9.x (or deepin 20.x)

## Install dependencies
```shell
sudo apt install texlive-lang-chinese texlive-lang-cjk texlive-xetex \
 latexmk texlive-latex-extra texlive-latex-recommended python-pip \
 texlive-latex-base texlive-plain-extra texlive-fonts-recommended \
 texlive-generic-recommended
```

## Python dependencies

```shell
sudo pip install Sphinx commonmark sphinx-rtd-theme
```

if download is too slow, try use local mirror

```shell
sudo pip install Sphinx commonmark sphinx-rtd-theme -i https://mirrors.aliyun.com/pypi/simple/
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

2. If occuring FreeXXX font not found

```sh
# for ubuntu
sudo apt install fonts-freefont-otf

# for fedora
sudo dnf install texlive-gnu-freefont
```
