from jivago.lang.annotations import Inject
from jivago.lang.registry import Component
from jivago.wsgi.annotations import Resource


@Component
class CalculatorClass(object):

    def do_calculation(self) -> int:
        return 4


@Resource("/calculation")
class CalculatedResource(object):

    @Inject
    def __init__(self, calculator: CalculatorClass):
        self.calculator = calculator
