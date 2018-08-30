import random
from typing import List

from jivago.lang.annotations import Override, Inject
from jivago.lang.registry import Component


class Calculator(object):

    def do_calculation(self, input: int) -> int:
        raise NotImplementedError


@Component
class ConstantCalculator(Calculator):

    @Override
    def do_calculation(self, input: int) -> int:
        return 5


class RandomCalculator(Calculator):

    @Override
    def do_calculation(self, input: int) -> int:
        return random.randint(0, 100)


@Component
class CalculationService(object):

    @Inject
    def __init__(self, calculators: List[Calculator]):
        self.calculators = calculators

    def calculate(self, input: int) -> List[int]:
        return [calculator.do_calculation(input) for calculator in self.calculators]
