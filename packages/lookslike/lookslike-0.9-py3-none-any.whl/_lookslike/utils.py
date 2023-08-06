def filter_keys(keys):
    """
    Restrict comparison of Dictionaries to the given keys.

    :param keys: The keys
    :type keys: list of str
    :return: Dictionary that only contains the keys.
    :rtype: dict
    """
    def _filter_keys(dictionary):
        assert isinstance(dictionary, dict)
        return {key: value for key, value in dictionary.items() if key in keys}
    return _filter_keys
