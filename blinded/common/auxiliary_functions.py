import os
import random
import string


def write_dict_to_csv(save_path, dict_to_save):
    """Writes a dictionary to a csv

    :param save_path: full path directory, including filename and extension for saved file
    :param dict_to_save: list that will be saved into file provided in saveFullFilename
    :return: save_path
    """

    with open(save_path, 'w') as f:
        for key, value in dict_to_save.items():
            if type(value) is dict:
                f.writelines("{},{},{}".format(key, value['reviewer'], value['mask']))
                f.write('\n')
                continue
            f.writelines("{},{}".format(key, value))
            f.write('\n')
        f.close()


def read_file(file):
    """Reads a file, splitting at each line

    :param file: file path
    :return: List containing all lines of file
    """
    with open(file) as f:
        return f.read().splitlines()


def random_string_generator(len_string=10):
    """Generates a random string of length len_string.

    String will contain only lowercase letters and digits.

    :param len_string: length of returned string (default 10)
    :return: string of length len_string
    """

    lowercase_letters_and_digits = list(string.ascii_lowercase + string.digits)
    return ''.join(random.choices(lowercase_letters_and_digits, weights=None, k=len_string))


def write_list_to_csv(save_path, list_to_save):
    """Writes a list (any size) to a csv

    :param save_path: full path directory, including filename and extension for saved file
    :param list_to_save: list that will be saved into file provided in saveFullFilename
    :return: save_path
    """

    with open(save_path, 'w') as f:
        for item in list_to_save:
            f.writelines("%s," % entry for entry in item)
        f.close()


def get_subjects(data_dir, subj_flag='et'):
    return set([item.strip('et') for item in os.listdir(data_dir) if item.startswith(subj_flag)])