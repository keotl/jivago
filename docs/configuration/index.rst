Application Configuration
==========================

Configuration is done using a context class, which defines various methods which can be overridden. The recommended way of defining an application context is by inheriting from either ``ProductionJivagoContext`` or ``DebugJivagoContext``, and overriding specific methods.

.. literalinclude:: context.py
   :language: python


Configuration methods
---------------------

configure_service_locator()
  This method can be used to manually bind classes to the internal ServiceLocator. See `Dependency Injection`_ for more details.

.. _Dependency Injection: ../dependency_injection/index.html

scopes()
  This method defines component scopes for the ServiceLocator which determine when to instantiate new components. By default, only the ``Singleton`` exists.

get_filters()
  This method returns a list of Filters which should be applied to a specific request. It is called once for every request.

get_views_folder_path()
  This method defines the folder in which template files are stored for ``RenderedView`` responses. Defaults to the ``views`` submodule of the root package.

get_config_file_locations()
  Defines a list of files which should be tried when importing the application properties. The ``ApplicationProperties`` is creating using the first existent file in this rule. Defaults to ``["application.yml", "application.json", "properties.yml", "properties.json"]``.

create_router_config()
  This method is used to configure the ``Router`` object which is used to resolve requests. See `Router Configuration`_ for details.

.. _Router Configuration: router/index.html

get_default_filters()
  Used only on subclasses of ``ProductionJivagoFilter``. This method is called from ``create_router_config`` to define the default ``FilteringRule``.

create_event_bus()
  Used to register event handlers.

get_banner()
  Defines the ASCII-art banner which is printed in the console at every startup.

.. toctree::
   ../dependency_injection/index
   router/index

ApplicationProperties and SystemEnvironmentProperties
-----------------------------------------------------

Both the ``ApplicationProperties`` and ``SystemEnvironmentProperties`` dictionaries can be injected into a component class, thus providing access namely to the contents of the application config file, and to the environment variables. For instance, for an ``application.yml`` file placed in the working directory, an appropriate ``ApplicationProperties`` object is created.

*application.yml*

.. literalinclude:: application.yml
   :language: yaml

*my_component.py*

.. literalinclude:: properties.py
   :language: python



