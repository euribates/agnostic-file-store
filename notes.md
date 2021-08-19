### Update Pypip

```
pip install --upgrade pip
python -m build
ls dist/
pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
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
