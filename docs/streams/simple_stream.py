from jivago.lang.stream import Stream

# Result : [4, 16, 36]
square_of_even_numbers = Stream([1, 2, 3, 4, 5, 6]) \
    .filter(lambda x: x % 2 == 0) \
    .map(lambda x: x ** 2) \
    .toList()
