import re


if hasattr(re, 'Pattern'):
    def is_regex_pattern(obj):
        return isinstance(obj, re.Pattern)
else:
    def is_regex_pattern(obj):
        return "SRE_Pattern" in str(type(obj))


class Like:
    """
    Compare an object with something which is similar (but not equal) to it.

    :param args: One or multiple criteria that have to match
    :type args: type | Callable[[Any], bool] | re.Pattern | Any
    :param convert: Optional: A function to convert the comparison value before matching
    :type convert: Callable[[Any], Any]

    Example:
        # Directly compare values:
        42 == Like(int)  # True

        # Compare nested values:
        {'num': 42, 'alph': 'abcd'} == {'num': Like(int), 'alph': Like(str)} # -> True
    """

    def __init__(self, *args, convert = None):
        self._comparison_values = args
        self._convert = convert

    def __eq__(self, other):
        for comparison_value in self._comparison_values:
            if not self._compare_single_value(comparison_value, other):
                return False
        return True

    def _compare_single_value(self, comparison_value, other) -> bool:
        if self._convert is not None:
            other = self._convert(other)
        if isinstance(comparison_value, type):
            return isinstance(other, comparison_value)
        elif callable(comparison_value):
            return comparison_value(other)
        elif is_regex_pattern(comparison_value):
            if isinstance(other, (str, bytes)):
                stringified_value = other
            else:
                stringified_value = str(other)
            try:
                match = comparison_value.match(stringified_value)
            except TypeError:
                # This happens for b"ab" != Like(re.compile('ab')):
                # TypeError: cannot use a string pattern on a bytes-like object
                return False
            if match is None:
                return False
            return match.start() == 0 and match.end() == len(stringified_value)
        return type(other) == type(comparison_value) and other == comparison_value

    def __ne__(self, other):
        return not other == self
