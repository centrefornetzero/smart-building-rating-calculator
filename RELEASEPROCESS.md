The library is hosted on pypi
The library uses semantic versioning in `setup.py`

## Releasing the library
- Run `pip install twine`
- Run `pip install wheel`
- Run `python setup.py sdist bdist_wheel`
- Run `twine upload dist/*`
