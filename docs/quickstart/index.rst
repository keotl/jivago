Quickstart
===========

A minimal Jivago application is created as follows:

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
The resource class is the fundamental way of declaring API routes. To define a route, simply declare the path inside the ``@Resource`` decorator on the class. Sub-paths can be defined on any of the class' methods using the ``@Path`` decorator.
Unlike some other web frameworks, allowed HTTP methods have to be explicitly defined for each routing function. Use ``@GET``, ``@POST``, ``@PUT``, ``@DELETE``, etc. 



Serialization
--------------


Dependency Injection
----------------------



