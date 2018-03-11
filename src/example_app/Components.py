from jivago.lang.annotations import Component, Override


@Component
class MyComponent(object):

    def __init__(self, inte=5):
        self.inte = inte

    def returnTen(self):
        return 10


class MyChildClass(MyComponent):

    @Override
    def returnTen(self):
        return "TEN"
