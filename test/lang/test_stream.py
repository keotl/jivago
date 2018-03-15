import unittest

from jivago.lang.stream import Stream


class StreamTest(unittest.TestCase):
    COLLECTION = [5, 3, 1, 10, 51, 42, 7]
    DIVIDES_BY_THREE = lambda x: x % 3 == 0

    def setUp(self):
        self.stream = Stream(self.COLLECTION)

    def test_whenMapping_thenReturnFunctionAppliedToAllElements(self):
        expected = [x for x in map(StreamTest.DIVIDES_BY_THREE, self.COLLECTION)]

        result = self.stream.map(StreamTest.DIVIDES_BY_THREE).toList()

        self.assertEqual(expected, result)

    def test_whenFiltering_thenReturnElementsWhichEvaluateToTrue(self):
        expected = [x for x in filter(StreamTest.DIVIDES_BY_THREE, self.COLLECTION)]

        result = self.stream.filter(StreamTest.DIVIDES_BY_THREE).toList()

        self.assertEqual(expected, result)

    def test_givenAnElementThatMatches_whenCheckingAnyMatch_thenReturnTrue(self):
        result = self.stream.anyMatch(StreamTest.DIVIDES_BY_THREE)

        self.assertTrue(result)

    def test_givenNotAllElementsMatch_whenCheckingAllMatch_thenReturnFalse(self):
        result = self.stream.allMatch(StreamTest.DIVIDES_BY_THREE)

        self.assertFalse(result)

    def test_givenAllMatchingElements_whenCheckingAllMatch_thenReturnTrue(self):
        always_true = lambda x: True

        result = self.stream.allMatch(always_true)

        self.assertTrue(result)

    def test_givenNoMatchingElements_whenCheckingAnyMatch_thenReturnFalse(self):
        always_false = lambda x: False

        result = self.stream.anyMatch(always_false)

        self.assertFalse(result)

    def test_whenCollectingToSet_thenReturnASetContainingAllElements(self):
        result_set = self.stream.toSet()

        self.assertEqual(len(self.COLLECTION), len(result_set))
        for item in self.COLLECTION:
            self.assertTrue(item in result_set)


if __name__ == '__main__':
    unittest.main()
