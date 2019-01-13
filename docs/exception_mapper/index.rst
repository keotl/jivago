Error handling with exception mappers
=========================================
For basic error handling, Jivago provides an ``ExceptionMapper`` mechanism, which can automatically create an HTTP response for an uncaught exception. To define a custom exception mapper, create a component which inherits from the ``ExceptionMapper`` interface, implementing the *handles* and *create_response* methods. 

.. literalinclude:: exception_mapper.py
   :language: python

* *handles(exception) -> bool* : Used to find the corresponding exception mapper.
* *create_response(exception) -> Response* : Creates the actual HTTP response.
