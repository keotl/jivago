Global Event Bus
=================
For event-driven programming purposes, Jivago provides a simple ``EventBus`` interface which can be used from anywhere to trigger events and dispatch messages. This approach has the benefit of completely decoupling the *caller* from the *callee(s)*, which can be beneficial in some large-scale applications. Take a look at the following code snippet :

.. literalinclude:: event_bus.py
   :language: python

In this example, a call to ``/kill-player`` triggers an event named ``Player:Death``, thereby invoking all known handlers.

Event payload parameter and handler responses
--------------------------------------------------
The ``emit`` and handler methods accepts zero or one argument. In the event (*pun intended*) that said *payload* parameter is supplied while emitting the event, it shall be passed to all handlers which require it. Note that only a single payload parameter is allowed.

.. literalinclude:: payload.py
   :language: python

Should event handlers return something, responses are returned to the caller in the form of a tuple containing all non-nil responses. Note that this behaviour is not applicable when using the asynchronous (*async*) event bus.

Event handler types
---------------------
Event handlers can be implemented using any of the usual ways. Functions, methods and runnable classes are allowed. Since *EventHandlerClass* and *Runnable* objects are instantiated by the service locator, constructor injection is supported as usual.

.. Literalinclude:: handler_types.py
   :language: python


*Synchronous* vs *Asynchronous* event dispatching
-------------------------------------------------
By default, all events are handled **synchronously**, i.e. on the caller thread. Therefore, calling *EventBus.emit()* will only return once all handlers have been called. When *asynchronicity* is desired, events should be emitted using the ``AsyncEventBus``. 

.. literalinclude:: async_bus.py
   :language: python

Unlike the usual *EventBus.emit()*, *AsyncEventBus.emit()* returns immediately and returns nothing. Events are then dispatched by a thread pool executor, which can be configured in your application context.
