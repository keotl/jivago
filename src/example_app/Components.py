from jivago.inject.registry import Component, Singleton
from jivago.lang.annotations import Override, Inject


@Component
class MyComponent(object):

    @Inject
    def __init__(self, inte=5):
        self.inte = inte

    def returnTen(self):
        return 10


@Component
@Singleton
class MyChildClass(MyComponent):

    @Inject
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    @Override
    def returnTen(self) -> str:
        return self.message
