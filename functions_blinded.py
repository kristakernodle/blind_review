#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import re
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

    String will contain only lowercase letters and digits.

    :param len_string: length of returned string (default 10)
    :return: string of length len_string
    """

    lowercase_letters_and_digits = list(string.ascii_lowercase + string.digits)
    return ''.join(random.choices(lowercase_letters_and_digits, weights=None, k=len_string))


def decorator_get_all_files_review_status(dec_subject_flag, dec_session_dir_flag, dec_filetype, dec_filename_regex):
    def decorator(function):
        def wrapper(data_dir, subject_flag=dec_subject_flag, session_dir_flag=dec_session_dir_flag,
                    filetype=dec_filetype, filename_regex=dec_filename_regex):
            print(dec_subject_flag)
            return function(data_dir, subject_flag, session_dir_flag, filetype, filename_regex)

        return wrapper
    return decorator


@decorator_get_all_files_review_status('et', 'Training', '.csv', '\S+_\S+_\S+_\S+_\S+')
def get_all_files_review_status(data_dir, subject_flag, session_dir_flag, filetype, filename_regex):
    """Get a list of reviewed files and a list of not reviewed files

    :param str data_dir: full path of directory containing all subjects
    :param str subject_flag: flag in all subject directory names
    :param str session_dir_flag: flag in all session directory names
    :param str filetype: review file type
    :param str filename_regex: regex for filenames

    :return list not_reviewed_files: list of the full path for files that have not been reviewed
    :return list reviewed_files: list of the full path for files that have been reviewed

    """
    not_reviewed_files = []
    reviewed_files = []

    subject_dirs = [entry for entry in os.listdir(data_dir) if entry.startswith(subject_flag)]

    for subject in subject_dirs:

        subject_id = subject.strip(subject_flag)
        subject_dir = data_dir + subject
        subject_session_dir = os.path.join(subject_dir, session_dir_flag)
        if not os.path.isdir(subject_session_dir):
            continue

        for current_session in os.listdir(subject_session_dir):

            current_session_dir = os.path.join(subject_session_dir, current_session)
            if not os.path.isdir(current_session_dir):
                continue

            current_session_files = [file for file in os.listdir(current_session_dir) if file.endswith(filetype)]

            for file in current_session_files:
                if re.search(filename_regex, file):
                    reviewed_files.append(os.path.join(current_session_dir, file))
                    continue
                not_reviewed_files.append(os.path.join(current_session_dir, file))
