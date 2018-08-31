from jivago.config.abstract_context import AbstractContext
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Inject
from jivago.lang.registry import Component


@Component
class Calculator(object):
    def do_calculation(self) -> int:
        return 5

# ServiceLocator injection
@Component
class CalculationService(object):

    @Inject
    def __init__(self, service_locator: ServiceLocator):
        self.service_locator = service_locator
        self.calculator = self.service_locator.get(Calculator)


# Static access to the ServiceLocator object from anywhere
def calculate() -> int:
    service_locator = AbstractContext.INSTANCE.service_locator()
    calculator = service_locator.get(Calculator)
    return calculator.do_calculation()
