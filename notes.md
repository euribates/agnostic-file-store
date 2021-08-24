### Update Pypip

```
pip install --upgrade pip distutils
python -m build
ls dist/
pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
```

Si `python -m build` falla, instalarlo:

```shell
python3 -m pip install --upgrade build
```

### Instalat la libreria localmente

Develop mode is really, really nice:

```shell
$ python setup.py develop
```

or:

```shell
$ pip install -e ./
```

The `-e` stands for **editable** -- it is the same thing. It puts a link
(actually `*.pth` files) into the python installation to your code, so that your
package is installed, but any changes will immediately take effect.

This way all your test code, and client code, etc, can all import your package the usual way. No `sys.path` hacking

- Source: [Python Packaging tutorial](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)

tags: pip, develop

### Como actualizar la version disponile


1) Actualizar el número de versión, por ahora hay que tocar el fichero `setup.py` y el
fichero `src/afs/__init__.py`.

2) Make sure you have the latest version of PyPA’s build installed:

Si no:

```
python -m pip install --upgrade build
```

Ejecutar `build`como comando:

```
python -m build
```

Debería generar los archivos con los nombres adecuados en la carpeta `dist`. Por ejemplo,
para la versión `0.5.1` generó los archivos:

- `dist/agnostic_file_store-0.5.1-py3-none-any.whl`
- `dist/agnostic-file-store-0.5.1.tar.gz`

El fichero `tar.gz` is un archivo de fuentes mientras que el fichero `.whl` es una
distribución
prefabricada. Las versiones más recientes de pip prefieren usar la distribucion prefabricada
y solo si esta lfalla recurren a la distribución de las fuentes. Siempre es deseable
proporcionar distribuciones prefabricadas para todas las plataformas para las que sea
compatible nuestro proyecto. En este caso, este proyecto es solo Python, sin dependencias
binarias, asique solo necesitamos un único fichero prefabricado.

### Subir los archis de distribución a PyPi

(Tienes que tenere una cuanta activa en Pypi.org)

Usaremos [twine](https://packaging.python.org/key_projects/#twine) para subir la
distribución y hacerla pública. Podemos instalar/actualizar `twine` con:

```
python -m pip install --upgrade twine
```

Y luego subir los ficheros de distribucion con:

```
python3 -m twine upload --repository testpypi dist/*
```

Para subirlos al repositorio de prueba y:

```
python3 -m twine upload --repository pypi dist/*
```

Para subir y publicar en el repositorio oficial.







### How to maintain the version number in just one place

```python

def get_version():
    version_file = "src/_version.py"
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]
```

Content if `src/PIL/_version.py`:

```python
# Master version for Pillow
__version__ = "8.4.0.dev0"
```



    https://docs.python-guide.org/writing/license/
