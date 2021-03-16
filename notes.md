def get_version():
    version_file = "src/PIL/_version.py"
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]



    https://docs.python-guide.org/writing/license/
