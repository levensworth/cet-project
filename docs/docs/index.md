# KMusic: Sistema de recomendación para música.

Esta es la página oficial de `kmusic`, aquí podrás encontrar toda la información sobre el desarrollo
y funcionamiento del sistema.

## Como utilizar el repositorio:
1. Tener el interprete de `python` instalado en su computadora, para la versión 3.10
2. Tener un editor de texto para desarrollo, `VSCode` es el que recomendamos.
3. Instalar `poetry` es una herramienta de manjo de dependencias. Pueden instalarlo con el comando

```sh
pip install poetry
```

4. Descargar el repositorio, pueden hacerlo directo desde la web de github.
5. Desde una terminal, navegar hasta el principio del proyecto. (Estar dentro de la carpeta que descargaron.)
6. Correr el siguiente comando desde la terminal:
```sh
poetry install
```
7. Un vez que el proyecto esté instalado, es cuestión de correrlo:
```sh
poetry run uvicorn mission_control:app 
```
Al finalizar esto, deberán ver un mensaje en la terminal diciendoles en que url pueden acceder.

## Layout:
```
.
├── data
│   └── 1m_music_dataset.zip
├── docs
│   ├── docs
│   │   └── index.md
│   └── mkdocs.yml
├── lab
│   └── eda.ipynb
├── mission_control.py
├── poetry.lock
├── pyproject.toml
├── readme.md
├── requirements.txt
├── setup.cfg
├── src
│   ├── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── knn_engine_impl.py
│   └── main.py
├── templates
│   ├── index.jinja2
│   ├── recommendation.jinja2
│   ├── search-item.jinja2
│   └── search-results.jinja2
└── tests
```


El código se encuentra disponible bajo la carpeta `src`. Dentro de la misma encontraremos varios archivos, 
pero lo más importante es entender `main.py` y `knn_engine_impl.py`. El primero contiene la lógica que 
utilizamos para mostrar la web, y el segundo cotiene la implementación del sistema de recomendación que creamos.

En la sección de `lab` encontraremos un notebook con la experimentación sobre el dataset que utilizamos, el mismo se encuentra bajo la carpeta `data`.



