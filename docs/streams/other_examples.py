from jivago.lang.stream import Stream

first_ten_square_numbers = Stream.range() \
    .map(lambda x: x ** 2) \
    .take(10)
# [1, 4, 9, 16, 25, ...]


Stream.zip(['a', 'b', 'c'], [1, 2, 3]) \
    .forEach(lambda letter, number: print(f"{letter} is the {number}th letter of the alphabet."))

Stream.of(1, 2, 3, 4).allMatch(lambda x: x < 10)
# True


def square(x: int) -> int:
    return x ** 2


squares = Stream.of(1, 2, 3, 4).map(square).toList()
# [1, 4, 9, 16]

alphabet = Stream([(1, 'a'), (2, 'b'), (3, 'c')]).toDict()
# { 1 : 'a', ...}
