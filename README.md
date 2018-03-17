# Jivago Framework
## Dependency Injection (WIP)
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
