Reflection
===========

.. toctree::
   :maxdepth: 2


Jivago provides its own *reflection*-style registration mechanism. We will define as *annotations* decorators which do not alter the decorated functions or classes but add a means of programmatically inspecting said decorated functions or classes.

Accessing annotated elements is done by interrogating the *Registry* object. Two types of annotations are defined in Jivago :

 * `Annotation`: A general-purpose registering decorator.
 * `ParametrizedAnnotation`: Allows the passing of arguments when the annotation is used.

The *Registry* object contains references to all annotated elements, and provides a ``get_annotated_in_package`` method, which returns all registrations for a specific annotation, for which the package name starts with the given string. Below is an example where all classes with the ``@Component`` annotation in any package are requested. 

.. literalinclude:: registry.py
   :language: python


Declaring Custom Annotations
-------------------------------
Standard annotations can be defined using either the python-esque *decorator-style syntax* by adding the ``@Annotation`` decorator to a simple pass-through decorator, or the simpler *object-style syntax* by invoking the Annotation constructor. 

.. literalinclude:: annotations.py
   :language: python


Parametrized annotations can only defined using the decorator-style syntax. To create a new parametrized annotation, use the ``@ParametrizedAnnotation`` decorator on a function which returns a pass-through function. (See the example below.)

**When using the parametrized annotation, all parameters should be passed as keyword arguments. An unnamed argument will be saved in the dictionary as "value".**

.. literalinclude:: parametrized_annotations.py
   :language: python
