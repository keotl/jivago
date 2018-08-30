Quickstart
===========

A minimal Jivago application is shown below :

.. literalinclude:: minimal.py
   :language: python

Notice that the example is made up of three separate parts:

* A ``Resource`` class, which defines a route for our application;
* The ``JivagoApplication`` object, which contains the application itself;
* A ``__main__`` function which runs our application in a debug environment, listening on port 4000.

Now, pointing a web browser to ``http://localhost:4000`` should print our ``Hello World!`` message.

Component Auto-discovery
--------------------------

While defining our resource classes in our main file is definitely possible, it can become quite unwieldy. In fact, one of the key goals of the Jivago framework is to maintain loose-coupling of our components.

We will therefore move our resource classes into their own files, and use Jivago's built-in package discovery mechanism to automatically register our routes.

*hello_resource.py*

.. literalinclude:: simple_resource.py
   :language: python

*application.py*

.. literalinclude:: minimal_wsgi.py
   :language: python

.. code-block:: txt

   my_hello_world_application
    ├── __init__.py
    ├── application.py
    └── resources          
        ├── __init__.py
        └── hello_resource.py

Note that, when creating the JivagoApplication object, a reference to the application's root package is passed as the first argument. The root package should contain *all* Jivago-annotated classes. (i.e. ``@Resource``, ``@Component``, etc.)

**Warning :** Since all python files are imported at run-time, any lines of code outside a class or a function will be executed before the application is started. It is therefore highly advised to avoid having any line of code outside a declarative block. 

The Resource Class
--------------------
The resource class is the fundamental way of declaring API routes. To define a route, simply declare the path inside the ``@Resource`` decorator on the class. Sub-paths can be defined on any of the class' methods using the ``@Path`` decorator. Allowed HTTP methods have to be explicitly defined for each routing function. Use ``@GET``, ``@POST``, ``@PUT``, ``@DELETE``, etc.

Unlike other Python web framework, method invocation relies heavily on type annotations, which resemble the static typing present in other languages like C++ and Java. Given missing parameters, a method will not be invoked and simply be rejected at the framework level. For instance, declaring a route receiving a ``dict`` as a parameter matches a JSON-encoded request body. ``Request`` and ``Response`` objects can be requested/returned, when having direct control over low-level HTTP elements is required. 

When resolving string and numeric parameters, path parameters and query parameters are tried. In that case, the key should match the parameter variable name.

*A complex resource example*

.. literalinclude:: complex_resource.py
   :language: python

While return type annotations are not strictly required, they are nonetheless recommended to increase readability and enforce stylistic consistency.

Serialization
--------------
Jivago supports the definition of *DTO* classes, which can be directly serialized/deserialized. These classes explicitly define a JSON schema and attribute typing, negating the need to use an external schema validator. To define a DTO, use the ``@Serializable`` decorator :

.. literalinclude:: dto.py
   :language: python


If a constructor is declared, it is used when deserializing. Otherwise, each attribute is set using ``__setattr__``.

Dependency Injection
----------------------
To allow for modularity and loose-coupling, dependency injection is built into the framework. Resource classes can therefore request dependencies from their constructor.

.. literalinclude:: dependency_injection.py
   :language: python

``@Component`` is a general-purpose annotation which registers a class to the internal service locator. Whenever a class requires dependencies from their constructor, those get recursively instantiated and injected. Note that the ``@Inject`` annotation is required.

See `Dependency Injection`_ for advanced configurations.

.. _Dependency Injection: ../dependency_injection/index.html

View Rendering
---------------
Jivago also supports rendered HTML views, using the Jinja2 templating engine. 

*templated_resource.py*

.. literalinclude:: rendered_view_resource.py
   :language: python

*my-template.html*

.. literalinclude:: template.html
   :language: html

By default, the framework looks for a ``views`` package directly underneath the root package. 

.. code-block:: txt

   my_hello_world_application
    ├── __init__.py
    ├── application.py
    └── views          
        ├── __init__.py
        └── my-template.html
