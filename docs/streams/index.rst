Functional-style operations using Streams
=============================================
Jivago provides a ``Stream`` class which can be used to perform functional-style operations on collections. This mechanism is heavily inspired by *Java*'s identically named *Streams*.

.. literalinclude:: simple_stream.py
   :language: python

In the previous example, the usual *filter* and *map* operations are used in a sequential manner. While all these operations are all available in Python, using Jivago's *Streams* allows the chaining of these operations to improve readability.

All available functions are documented in `jivago.lang.stream`_.

.. _jivago.lang.stream: ../source/jivago.lang.stream.html

Other examples
---------------
.. literalinclude:: other_examples.py
   :language: python
