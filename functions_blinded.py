#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import string

__author__ = "Krista Kernodle"
__copyright__ = "Copyright 2020, The Leventhal Lab"
__credits__ = ["Krista Kernodle", "DeepLabCut", "B-SOiD"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Krista Kernodle"
__email__ = "kkrista@umich.edu"
__status__ = "Development"


def random_string_generator(len_string=10):
    """Generates a random string of length len_string.

    :param len_string: length of returned string (default 10)
    :return: string of length len_string
    """
    # random_string_generator(len_string=10) returns a string of len_string (default length = 10 characters). String will contain only lowercase letters and digits
    lowercase_letters_and_digits = list(string.ascii_lowercase + string.digits)
    return ''.join(random.choices(lowercase_letters_and_digits, weights=None, k=len_string))


def mask_file(original_fullpath, destination):
    if ~os.path.exists(destination):
        os.makedirs(destination)

    filename = os.path.basename(original_fullpath)