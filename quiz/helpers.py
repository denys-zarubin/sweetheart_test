import random
import string


def generate_random_text(length=15):
    """
    :param length: Default 15
    :return: Random string
    """
    return "".join(
        [random.choice(string.letters[:26]) for i in xrange(length)]
    )


def calculate_percent(val, total):
    """
    Used to calculate how much in percent is value
    """
    return int(val / float(total) * 100)
