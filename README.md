# Jivago Framework
![travis-ci](https://travis-ci.org/keotl/jivago.svg?branch=master)

For writing complex, robust Python backend applications. Inspired by Spring, Jersey, hk2, and the like. Also includes other Java-esque goodies, such as stream operations.


Below is what currently works.
## HTTP Resource
```python
from example_app.comp.beans import SomeBean
from jivago.lang.annotations import Inject
from jivago.wsgi.methods import GET, POST, DELETE
from jivago.wsgi.router import Resource, Path


@Resource("/hello")
class HelloWorldResource(object):

    @Inject
    def __init__(self, some_bean: SomeBean):
        self.some_bean = some_bean

    @GET
    def get_hello(self) -> str:
        return self.some_bean.say_hello()

    @POST
    @Path("/{name}")
    def post_hello(self, name: str) -> str:
        print("name: {}".format(name))
        return self.some_bean.say_hello()

    @Path("/delete")
    @DELETE
    def delete_hello(self) -> str:
        return self.some_bean.say_hello()

    @Path("/dto")
    @POST
    def with_dto(my_dto: MyDto) -> AnotherDto:
        return AnotherDto(my_dto.name)

```
## Using defined DTOs
```python
from jivago.lang.annotations import Serializable


@Serializable
class MyDto(object):
    name: str
    age: int

@Serializable
class AnotherDto(object):
    name: str
    def __init__(self, name: str): # Or with an explicit constructor
        self.name = name
```
## Background Worker Threads
```python
@BackgroundWorker
class Worker(Runnable):
    @Inject
    def __init__(self, some_bean: SomeBean):
        self.some_bean = some_bean
    def run(self):
        print("hello")
```
## Dependency Injection

### Using a standalone Service Locator
Requires type hints to be used!
```python
class MyConcreteClass(MyAbstractClass):
    @Inject
    def __init__(self):
        self.value = 5

service_locator = ServiceLocator()
service_locator.bind(MyAbstractClass, MyConcreteClass)
service_locator.get(MyAbstractClass) # Instantiates the object by recursively injecting constructor dependencies.
```
Component auto-discovery.
```python
@Component
class MyComponent(object):
    @Inject
    def __init__(self, a_singleton: MySingletonComponent):
        self.dep = a_singleton

@Component
@Singleton    # This component will be lazily instantiated and re-injected.
class MySingletonComponent(object):
    @Inject
    def __init__(self):
        self.content = []
```
Factory/Provider functions
```python
@Provider    # Uses the return type to determine when the function should be called.
def get_some_component(dependency: MyComponent) -> MyOtherComponent:
    # Do some logic
    return MyOtherComponent()
```

### Other goodies
- Java-esque `@Override` annotation. (Has no logic _per se_.)
```python
class MyInterface(object):
    def get_message() -> str:
        raise NotImplementedError

class MyImplementation(MyInterface):
    @Override
    def get_message() -> str:
        return "hello"
```
+ Java-esque streams.
```python
Stream([5,3,1,3]).map(lambda x: x + 50).toList()
```
