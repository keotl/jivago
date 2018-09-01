# Jivago Framework - The Highly-Reflective Object-Oriented Python Web Framework
![travis-ci](https://travis-ci.org/keotl/jivago.svg?branch=master)
![readthedocs](https://readthedocs.org/projects/jivago/badge/?version=latest)
[![PyPI version](https://badge.fury.io/py/jivago.svg)](https://badge.fury.io/py/jivago)

Jivago is an object-oriented, highly-reflective Python framework for building web applications. It relies heavily on type annotations and decorators to enforce typing, providing package auto-discovery and dependency injection out of the box. This leads to less boilerplate code, while maintaining loose-coupling across components.

Also includes other Java-esque goodies, such as stream operations!

Find the documentation over at [jivago.readthedocs.io](https://jivago.readthedocs.io).

### Minimal Jivago Application
```python
from jivago.jivago_application import JivagoApplication
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/")
class HelloResource(object):

    @GET
    def get_hello(self) -> str:
        return "Hello World!"


app = JivagoApplication()

if __name__ == '__main__':
    app.run_dev()
```

### Installation
Requires Python3.6 or greater.
```bash
pip install jivago
```
