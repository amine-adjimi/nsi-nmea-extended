def check_type(item, t):
    """
    Validates that an object is an instance of a specific type and raises an error if it is not.

    :param item: The object to be checked
    :param t: The expected type of the object
    :return:
    :rtype: None
    """

    if not isinstance(item, t):
        raise TypeError(f"{str(item)} should be of type {t.__name__} but it is {type(item).__name__}")

def check_value(item, v):
    """
    Validates that an object matches a specific value or is contained within a set of allowed values and raises an error if it doesn't.

    :param item: The object to be checked
    :param v: The expected value of the object
    :return:
    :rtype: None
    """

    if isinstance(v, tuple):
        if item not in v:
            raise ValueError(f'{str(item)} should be {' or '.join(f'{str(vv)}' for vv in v)}')

    else:
        if item != v:
            raise ValueError(f'{str(item)} should be {str(v)}')

def check_both(item, t, v):
    """
    A wrapper for checkValue and check_type that performs both checks as one.

    :param item: The object to be checked
    :param t: The expected type of the object
    :param v: The expected value(s) of the object
    :return:
    :rtype: None
    """

    check_type(item, t)
    check_value(item, v)

def check_nmea_sum(sentence):
    """
    Validates that a NMEA sentence has a valid checksum and raises an error if it hasn't.

    :param sentence: The full raw NMEA sentence to be checked (e.g., "$GPRMC,145703.00,A,5043.67117,N,00232.08485,E,10.999,143.90,261218,,,A*55")
    :type sentence: str
    :return:
    :rtype: None
    """

    try:
        data = sentence[1:sentence.index("*")]
        expected = int(sentence[sentence.index("*")+1:], 16)

    except (ValueError, IndexError):raise ValueError(f'Checksum failed.')

    calculated = 0
    for car in data:
        calculated ^= ord(car)

    if calculated != expected:raise ValueError(f'Checksum rejected.')