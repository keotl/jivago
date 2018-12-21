Dependency Injection
======================
Jivago provides a powerful dependency injection engine as a means of implementing inversion of control.

Basic Usage
------------
Classes annotated with ``@Component`` or ``@Resource`` are automatically registered in the built-in service locator. Dependencies are constructor-injected, and require proper typing hints to be used.

.. literalinclude:: dependency_injection_example.py
   :language: python

Always make sure that the type hint corresponds exactly to the requested object. (i.e. The type annotation could be used directly as a constructor.) An identically-named, but otherwise different class will not work.

Collections
------------
Using a collection type hint, all children of a class can be requested. Take a look at the following example :


.. literalinclude:: collection_example.py
   :language: python


The *CalculationService* class is injected with a list of all components which implement the *Calculator* interface. 

Scopes
------
By default, all components are re-instantiated when a request is received. However, a ``@Singleton`` annotation is provided for when unicity is important. (e.g. when making a simple persistence mechanism held in memory.)

.. literalinclude:: singleton.py
   :language: python

A *singleton* component will be instantiated when it is first requested, and reused for subsequent calls.

Factory Functions
-------------------
When complex scoping is required for a given component, for example when handling a database connection, factory functions can be used to instantiate and cache components using the ``@Provider`` annotation. In this case, the return type hint defines the class to which the function is registered. 

.. literalinclude:: factory_functions.py
   :language: python

The provider function can take any registered component as arguments.

Manual Component Registration
--------------------------------
When fine-tuned control is necessary, the service locator should be manually configured by extending the *Context* object. In order to do so, first override either ``ProductionJivagoContext`` or ``DebugJivagoContext``. This will be your new application context, which should be passed to the JivagoApplication object. The ``configure_service_locator`` is where component registration is done. Use the ``self.serviceLocator.bind`` method to manually register components. Note that Jivago decorators will not be taken into consideration when using manual component registration.

.. literalinclude:: manual_registration.py
   :language: python

The ``bind(interface, implementation)`` methods registers an **implementation** to its **interface**. The service locator acts as a dictionary, where the *interface* is the key, and the *implementation* is the value. The interface should always be a class.

The *implementation* can be any of the following :
 * A class
 * An instance of a class
 * A function which, when called, returns an instance of a class

 When a class is given, the default behaviour is applied : a new instance is created whenever the interface is requested. Registering an instance of the class causes it to act as a singleton. Finally, a registered function will be invoked whenever the interface class is requested.

Service Locator Object
------------------------
Similarily, components can be manually requested by directly invoking the *ServiceLocator* object. A reference to the *ServiceLocator* object can be obtained either through dependency injection, or statically.

.. literalinclude:: service_locator.py
   :language: python

The service locator has ``get`` and ``get_all`` methods for requesting components.
