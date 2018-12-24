import unittest

from jivago.lang.stream import Stream


class StreamTest(unittest.TestCase):
    COLLECTION = [5, 3, 1, 10, 51, 42, 7]
    DIVIDES_BY_THREE = lambda x: x % 3 == 0
    BUMPY_COLLECTION = [[5, 3, 1], [10], [51, 42, 7]]

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

    def test_whenCollectingToList_thenReturnAListContainingAllElements(self):
        result_list = self.stream.toList()

        self.assertIsInstance(result_list, list)
        self.assertEqual(self.COLLECTION, result_list)

    def test_whenCollectingToSet_thenReturnASetContainingAllElements(self):
        result_set = self.stream.toSet()

        self.assertEqual(len(self.COLLECTION), len(result_set))
        self.assertIsInstance(result_set, set)
        for item in self.COLLECTION:
            self.assertTrue(item in result_set)

    def test_givenAListOfPairs_whenCollectingToDict_thenExpandPairsToKeyValue(self):
        dictionary = self.stream.map(lambda x: (x, StreamTest.DIVIDES_BY_THREE(x))).toDict()

        self.assertEqual(len(self.COLLECTION), len(dictionary.keys()))
        self.assertIsInstance(dictionary, dict)
        for i in self.COLLECTION:
            self.assertEqual(dictionary[i], StreamTest.DIVIDES_BY_THREE(i))

    def test_whenForEach_thenCallFunctionOnAllItems(self):
        result = []
        add_to_list = lambda x: result.append(x)

        self.stream.forEach(add_to_list)

        self.assertEqual(self.COLLECTION, result)

    def test_givenCollectionOfTuples_whenForEach_thenExpandTuplesWhenCallingFunction(self):
        result = []
        self.stream = Stream([(1, -1), (2, -2)])
        add_sum_to_list = lambda x, y: result.append(x + y)

        self.stream.forEach(add_sum_to_list)

        self.assertEqual([0, 0], result)

    def test_givenFunctionWithTwoParameters_whenMapping_thenExpandTuplesWhenCallingFunction(self):
        result = self.stream.map(lambda x: (x, x)).map(lambda x, y: x - y).toList()

        self.assertEqual([0 for i in self.COLLECTION], result)

    def test_givenFunctionWithTwoParameters_whenFiltering_thenExpandTuplesWhenCallingFunction(self):
        result = self.stream.map(lambda x: (x, x)).filter(lambda x, y: x == y).toList()

        self.assertEqual([(i, i) for i in self.COLLECTION], result)

    def test_givenFunctionWithTwoParameters_whenFindingFirstMatch_thenExpandTuplesWhenCallingFunction(self):
        result = self.stream.map(lambda x: (x, x)).firstMatch(lambda x, y: x == y)

        self.assertEqual((self.COLLECTION[0], self.COLLECTION[0]), result)

    def test_givenFunctionWithTwoParameters_whenIteratingOverScalars_thenThrowTypeError(self):
        with self.assertRaises(TypeError):
            self.stream.map(lambda x, y: x + y).toList()

    def test_givenStreamOfLists_whenFlattening_thenReturnStreamOfConcatenatedLists(self):
        result = Stream(self.BUMPY_COLLECTION).flat().toList()

        self.assertEqual(self.COLLECTION, result)

    def test_givenNoMatchingElements_whenCheckingNoneMatch_thenReturnTrue(self):
        always_false = lambda x: False

        result = Stream(self.COLLECTION).noneMatch(always_false)

        self.assertTrue(result)

    def test_givenMatchingElements_whenCheckingNoneMatch_thenReturnFalse(self):
        sometimes_true = lambda x: x % 2 == 0

        result = Stream(self.COLLECTION).noneMatch(sometimes_true)

        self.assertFalse(result)

    def test_givenMultipleIterables_whenCreatingStream_thenIterablesAreConcatenated(self):
        result = Stream(self.BUMPY_COLLECTION, self.COLLECTION).toList()

        self.assertEqual(self.BUMPY_COLLECTION + self.COLLECTION, result)

    def test_whenZipping_thenIterateOverTheCollectionsTwoByTwo(self):
        expected = [(1, 4), (2, 5), (3, 6)]

        result = Stream.zip([1, 2, 3], [4, 5, 6]).toList()

        self.assertEqual(expected, result)

    def test_givenTupleIteration_whenUnzipping_thenReturnSeparateLists(self):
        expected = ((1, 3, 5), (2, 4, 6))

        first_list, second_list = Stream([(1, 2), (3, 4), (5, 6)]).unzip()

        self.assertEqual(expected[0], first_list)
        self.assertEqual(expected[1], second_list)

    def test_whenCreatingFromNonIterableElements_thenCreateACollectionContainingAllParameters(self):
        result = Stream.of(1, 2, 3, 4).toList()

        self.assertEqual([1, 2, 3, 4], result)

    def test_whenCollectingToTuple_thenReturnATupleContainingTheCollection(self):
        result = Stream([1, 2, 3, 4, 5]).toTuple()

        self.assertIsInstance(result, tuple)
        self.assertEqual((1, 2, 3, 4, 5), result)

    def test_whenCalculatingSum_thenReturnSumOfCollection(self):
        stream_sum = self.stream.sum()

        self.assertEqual(sum(self.COLLECTION), stream_sum)

    def test_whenCheckingMinimum_thenReturnSmallestElementInTheCollection(self):
        smallest_element = self.stream.min()

        self.assertEqual(min(self.COLLECTION), smallest_element)

    def test_whenCheckingMaximum_thenReturnLargestElementInTheCollection(self):
        largest_element = self.stream.max()

        self.assertEqual(max(self.COLLECTION), largest_element)

    def test_whenCountingElementsOfACollection_thenReturnLengthOfCollection(self):
        count = self.stream.count()

        self.assertEqual(len(self.COLLECTION), count)

    def test_whenCountingElementsOfIterableWithoutLength_thenIndividuallyCountElements(self):
        self.stream = Stream(zip(self.COLLECTION, self.COLLECTION))

        count = self.stream.count()

        self.assertEqual(len(self.COLLECTION), count)

    def test_whenReducing_thenReturnFinalValueOfAccumulator(self):
        sum_reducer = lambda accumulator, element: accumulator + element

        reduction = self.stream.reduce(0, sum_reducer)

        self.assertEqual(sum(self.COLLECTION), reduction)

    def test_whenTaking_thenReturnStreamWithOnlyFirstElements(self):
        first_elements = Stream(range(0, 30)).take(5).toList()

        self.assertEqual([0, 1, 2, 3, 4], first_elements)

    def test_givenClassReference_whenMapping_thenCallClassConstructor(self):
        squares = Stream.of(1, 2, 3, 4).map(AClassWithAMethod).map(AClassWithAMethod.get_square).toList()

        self.assertEqual([1, 4, 9, 16], squares)

    def test_givenMethodWhichRequiresAParameter_whenMapping_thenInvokeMethodWithParameter(self):
        calculator_object = AClassWithAMethod(0)

        result = Stream.of(1, 2, 3, 4).map(calculator_object.increment).toList()

        self.assertEqual([1, 2, 3, 4], result)

    def test_givenMethodWhichRequiresTwoParameters_whenMapping_thenInvokeAndExpandParameters(self):
        calculator_object = AClassWithAMethod(0)

        result = Stream.zip([1, 2, 3, 4], [1, 2, 3, 4]).map(calculator_object.sum_of_two_values).toList()

        self.assertEqual([2, 4, 6, 8], result)

    def test_givenBuiltinFunction_whenMapping_thenCorrectlyExpandParametersAndDoNotCrash(self):
        expected = Stream(range(0, 4)).map(lambda x: ord(str(x))).toList()
        result = Stream.of("0", "1", "2", "3").map(ord).toList()

        self.assertEqual(expected, result)

    def test_givenBuiltinType_whenMapping_thenCallConstructorWithASingleParameter(self):
        result = Stream.of("1", "2", "3").map(int).toList()

        self.assertEqual([1, 2, 3], result)

    def test_givenMissingParameters_whenGettingRange_thenReturnInfiniteIterator(self):
        first_25 = Stream.range().take(25).toList()

        self.assertEqual([x for x in range(0, 25)], first_25)

    def test_givenParameters_whenGettingRange_thenPassParametersToBuiltinRange(self):
        first5 = Stream.range(5).toList()

        self.assertEqual([x for x in range(0, 5)], first5)

    def test_whenGettingFirst_thenReturnFirstElementInIterable(self):
        first = Stream.range().first()

        self.assertEqual(0, first)

    def test_givenEmptyStream_whenGettingFirst_thenReturnNone(self):
        first = Stream([]).first()

        self.assertIsNone(first)


class AClassWithAMethod(object):

    def __init__(self, value: int):
        self.value = value

    def get_square(self) -> int:
        return self.value ** 2

    def increment(self, x: int) -> int:
        return self.value + x

    def sum_of_two_values(self, x, y) -> int:
        return x + y
