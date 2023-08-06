[![Build Status](https://app.travis-ci.com/Aniro-Montenegro/libpythonpro.svg?branch=main)](https://app.travis-ci.com/Aniro-Montenegro/libpythonpro)

[![Updates](https://pyup.io/repos/github/Aniro-Montenegro/libpythonpro/shield.svg)](https://pyup.io/repos/github/Aniro-Montenegro/libpythonpro/)

[![Python 3](https://pyup.io/repos/github/Aniro-Montenegro/libpythonpro/python-3-shield.svg)](https://pyup.io/repos/github/Aniro-Montenegro/libpythonpro/)

# libpythonpro
Módulo para exemplificar construção de projetos Python no curso PyTools

Suportada versão 3 de Python

Aplicado interpretador

Reformular pastas

### Requimerents

pip freeze > requirements.txt

### Virtual Env

py -3 -m venv .venv

.venv\Scripts\activate

.venv\Scripts\deactivate.bat

### Pip Gerenciamento de pacotes

pip install requests- cria o arquivo requeriments

pip freeze  -verifica as bibliotecas instaladas até o momento

pip freeze > requirements.txt   — cria o arquivo requirements com as bibliotecas do projeto


pip install -r requirements.txt - instala as bibliotecas do projeto

### Flake8

pip install flake8

pip freeze > requirements-dev.txt

pip install -r requirements-dev.txt

flake8 - avalia o codigo

## Para Inatalar

````commandline
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
````

### Para Conferir qualidade do código
flake 8- Verifica qualidade de codigo
````commandline
flake8
````

# Upgrade de Dependencias

pip uninstall [requests] - Desistala biblioteca especifica(usas sem conchetes)

pip freeze

pip install requests==2.27.1 - Instala biblioteca especifica

##Travis
[![Build Status](https://app.travis-ci.com/Aniro-Montenegro/libpythonpro.svg?branch=main)](https://app.travis-ci.com/Aniro-Montenegro/libpythonpro)



##Criar release

git tag 0.1

git push --tags

###Criar ambiente virtual

````commandline
py -3 -m venv .venv
.venv\Scripts\activate
````
pip install https://github.com/Aniro-Montenegro/libpythonpro/archive/refs/tags/0.1.zip


##Publicacao Pypi

python setup.py sdist   -cria diretorio com minha distribuição

pip install twine

twine upload dist/*
