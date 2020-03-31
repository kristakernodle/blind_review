#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import re
import string
from pathlib import Path
import math
import shutil

__author__ = "Krista Kernodle"
__copyright__ = "Copyright 2020, The Leventhal Lab"
__credits__ = ["Krista Kernodle", "DeepLabCut", "B-SOiD"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Krista Kernodle"
__email__ = "kkrista@umich.edu"
__status__ = "Development"


def write_dict_to_csv(save_path, dict_to_save):
    """Writes a dictionary to a csv

    :param save_path: full path directory, including filename and extension for saved file
    :param dict_to_save: list that will be saved into file provided in saveFullFilename
    :return: save_path
    """

    with open(save_path, 'w') as f:
        for key, value in dict_to_save.items():
            f.writelines(f'{key}, {value},')
            f.write("\n")
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
    return [item for item in os.listdir(data_dir) if item.startswith(subj_flag)]


def __decorator_get_current_reviewers(dec_reviewer_folder_regex):
    def decorator(function):
        def wrapper(blind_dir, reviewer_folder_regex=dec_reviewer_folder_regex):
            return function(blind_dir, reviewer_folder_regex)

        return wrapper

    return decorator


@__decorator_get_current_reviewers('\S+_\S')
def get_current_reviewers(blind_dir, reviewer_folder_regex):
    current_reviewers = []
    for item in os.listdir(blind_dir):
        if not os.path.isdir(os.path.join(blind_dir, item)):
            continue
        if re.search(reviewer_folder_regex, item):
            current_reviewers.append(' '.join(item.split('_')))
    return set(current_reviewers)


def __decorator_get_all_files_review_status(dec_subject_flag, dec_session_dir_flag, dec_file_type, dec_filename_regex):
    def decorator(function):
        def wrapper(data_dir, subject_flag=dec_subject_flag, session_dir_flag=dec_session_dir_flag,
                    filetype=dec_file_type, filename_regex=dec_filename_regex):
            return function(data_dir, subject_flag, session_dir_flag, filetype, filename_regex)

        return wrapper

    return decorator


@__decorator_get_all_files_review_status('et', 'Training', '.csv', '\S+_\S+_\S+_\S+_\S+')
def get_all_files_review_status(data_dir, subject_flag, session_dir_flag, file_type, filename_regex):
    """Get a list of reviewed files and a list of not reviewed files

    :param str data_dir: full path of directory containing all subjects
    :param str subject_flag: flag in all subject directory names
    :param str session_dir_flag: flag in all session directory names
    :param str file_type: review file type
    :param str filename_regex: regex for filenames
    :returns: not_reviewed_files: list of the full path for files that have not been reviewed
    :returns: reviewed_files: list of the full path for files that have been reviewed

    """
    not_reviewed_files = []
    reviewed_files = []

    subject_dirs = [entry for entry in os.listdir(data_dir) if entry.startswith(subject_flag)]

    for subject in subject_dirs:
        subject_dir = os.path.join(data_dir, subject)
        subject_session_dir = os.path.join(subject_dir, session_dir_flag)
        if not os.path.isdir(subject_session_dir):
            continue

        for current_session in os.listdir(subject_session_dir):

            current_session_dir = os.path.join(subject_session_dir, current_session)
            if not os.path.isdir(current_session_dir):
                continue

            current_session_files = [file for file in os.listdir(current_session_dir) if file.endswith(file_type)]

            for file in current_session_files:
                if re.search(filename_regex, file):
                    reviewed_files.append(os.path.join(current_session_dir, file))
                    continue
                not_reviewed_files.append(os.path.join(current_session_dir, file))

    return reviewed_files, not_reviewed_files


def get_all_masked_files(blind_dir):
    reviewers = get_current_reviewers(blind_dir)
    for reviewer in reviewers:

        current_reviewer_dir = os.path.join(blind_dir, '_'.join(reviewer.split(' ')))
        current_reviewer_masks_dir = os.path.join(current_reviewer_dir, '.masks')

        if not os.path.exists(current_reviewer_masks_dir):
            # .masks DOES NOT exist
            #
            # Here is the code snippet for creating the .masks directory
            # if reviewer == 'Krista K':
            #     os.makedirs(current_reviewer_masks_dir)
            continue

        reviewer_value = reviewer[0] + reviewer[-1]
        masks_filename = 'masks_' + reviewer_value + '.csv'
        reviewer_masks = read_file(os.path.join(current_reviewer_masks_dir, masks_filename))
    return None


def mask_files(blind_dir, files_to_mask, reviewers, folder_flag='Reaches', proportion_files_per_reviewer=1):
    mask_key_dir = os.path.join(blind_dir, '.mask_keys')
    all_masked_files_by_reviewer = dict()
    file_mask_keys = dict()
    files_left_to_mask = files_to_mask
    master_file_keys = dict()
    master_file_keys_save_path = os.path.join(mask_key_dir, 'master_file_keys.csv')

    if not os.path.exists(mask_key_dir):
        os.makedirs(mask_key_dir)
        for reviewer in reviewers:
            reviewer_value = reviewer[0] + reviewer[-1]
            reviewer_mask_dir = os.path.join(mask_key_dir, 'mask_' + reviewer_value + '.csv')
            if not os.path.exists(reviewer_mask_dir):
                Path(reviewer_mask_dir).touch()
    else:
        print('ADDING THIS IN -- functionality not added')
        old_master_file_keys = read_file(master_file_keys_save_path)
        for old_pair in old_master_file_keys:
            file = old_pair.split(' ')[0]
            the_value = old_pair.split(':')
            reviewer = the_value[1]
            mask = the_value[-1]
            file_mask_keys[mask] = file
            master_file_keys[file] = {'reviewer': reviewer, 'mask': mask}
            if reviewer in all_masked_files_by_reviewer.keys():
                all_masked_files_by_reviewer[reviewer].add(file)
                continue
            all_masked_files_by_reviewer[reviewer] = {file}

    if proportion_files_per_reviewer != 1:
        print('Functionality not available yet')
        return False

    num_files_per_reviewer = math.floor(len(files_to_mask) / len(reviewers))
    for reviewer in reviewers:
        files_assigned_to_reviewer = random.sample(files_left_to_mask, num_files_per_reviewer)

        for file in files_assigned_to_reviewer:
            files_left_to_mask.pop(files_left_to_mask.index(file))
            _, ext = os.path.splitext(file)
            if reviewer in all_masked_files_by_reviewer.keys():
                all_masked_files_by_reviewer[reviewer].add(file)
                continue
            all_masked_files_by_reviewer[reviewer] = {file}

    while len(files_left_to_mask) >= 1:
        reviewer = random.sample(reviewers, 1)[0]

        file_assigned_to_reviewer = random.sample(files_left_to_mask, 1)[0]
        files_left_to_mask.pop(files_left_to_mask.index(file_assigned_to_reviewer))

        if reviewer in all_masked_files_by_reviewer.keys():
            all_masked_files_by_reviewer[reviewer].add(file_assigned_to_reviewer)
            continue
        all_masked_files_by_reviewer[reviewer] = {file_assigned_to_reviewer}

    for reviewer, all_assigned_files in all_masked_files_by_reviewer.items():
        reviewer_file_keys = dict()
        reviewer_value = reviewer[0] + reviewer[-1]
        reviewer_file_keys_save_path = os.path.join(mask_key_dir, 'mask_' + reviewer_value + '.csv')
        reviewer_to_score_dir = os.path.join(blind_dir, '_'.join(reviewer.split(' ')), 'toScore_' + reviewer_value)
        for file in all_assigned_files:
            # Set up the original folder contents for copying:
            if 'Reaches' in file:
                get_folder_num = file.split('Reaches')[-1]
                folder_num = get_folder_num[0:2]
                original_folder_dir = os.path.dirname(file)
            else:
                folder_num = file.split('_')[-1]
                folder_num = folder_num.strip('.csv')
                if len(folder_num) < 2:
                    folder_num = f'0{folder_num}'
                original_folder_dir = os.path.join(os.path.dirname(file), folder_flag + folder_num)

            original_folder_contents = [os.path.join(original_folder_dir, trial) for trial in os.listdir(original_folder_dir)]

            # Set up the new folder to copy into:
            new_filename = random_string_generator()
            while new_filename in file_mask_keys.keys():
                new_filename = random_string_generator()
            file_mask_keys[new_filename] = file
            masked_folder_dir = os.path.join(reviewer_to_score_dir, new_filename)
            Path(masked_folder_dir).mkdir(parents=True)

            # Copy into new folder
            masked_folder_contents = [os.path.join(masked_folder_dir, '{}_{}.{}'.format(new_filename, num, 'mp4')) for num in range(1, len(original_folder_contents)+1)]
            for orig_file, masked_file in zip(original_folder_contents, masked_folder_contents):
                shutil.copyfile(orig_file, masked_file)
                reviewer_file_keys[orig_file] = masked_file
                master_file_keys[orig_file] = {'reviewer': reviewer_value, 'mask': new_filename}

            write_dict_to_csv(reviewer_file_keys_save_path, reviewer_file_keys)

    write_dict_to_csv(master_file_keys_save_path, master_file_keys)

    return True

def files_by_assigned_reviewer(data_dir, blind_dir):
    reviewers = get_current_reviewers(blind_dir)
    [reviewed_files, _] = get_all_files_review_status(data_dir)
    # masked_files = get_all_masked_files(blind_dir)

    files_with_reviewers = dict()
    reviewers_dict = dict()
    for reviewer in reviewers:
        reviewers_dict[reviewer] = reviewer[0] + reviewer[-1]

    for file in reviewed_files:
        filename_wo_ext = os.path.splitext(file)[0]
        reviewer_value = filename_wo_ext[-2:]
        filename_wo_reviewer = filename_wo_ext[:-2]

        if filename_wo_reviewer in files_with_reviewers.keys():
            found_reviewers = files_with_reviewers[filename_wo_reviewer]
            found_reviewers.append(reviewer_value)
            files_with_reviewers[file] = found_reviewers
            continue
        files_with_reviewers[filename_wo_reviewer] = [reviewer_value]

    return files_with_reviewers
