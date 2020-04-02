import os
import random

from math import floor
from pathlib import Path
import shutil

from ..common.auxiliary_functions import write_dict_to_csv, read_file, random_string_generator


def get_all_masked_files(blind_dir):
    mask_key_dir = os.path.join(blind_dir, '.mask_keys')
    if not os.path.exists(mask_key_dir):
        return [], [], []
    master_file_key_path = os.path.join(blind_dir, '.mask_keys', 'master_file_keys.csv')
    master_keys = read_file(master_file_key_path)

    master_file_keys = dict()
    file_mask_keys = dict()
    all_masked_files_by_reviewer = dict()

    for pair in master_keys:

        file, reviewer, mask = pair.split(',')
        file_mask_keys[mask] = file
        master_file_keys[file] = {'reviewer': reviewer, 'mask': mask}
        if reviewer in all_masked_files_by_reviewer.keys():
            all_masked_files_by_reviewer[reviewer].add(file)
            continue
        all_masked_files_by_reviewer[reviewer] = {file}

    return master_file_keys, file_mask_keys, all_masked_files_by_reviewer


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
        [master_file_keys, file_mask_keys, _] = get_all_masked_files(blind_dir)

    if proportion_files_per_reviewer != 1:
        print('Functionality not available yet')
        return False

    num_files_per_reviewer = floor(len(files_to_mask) / len(reviewers))
    for reviewer in list(reviewers):
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
                if int(folder_num) == 0:
                    print(file)
                    continue
                elif len(folder_num) < 2:
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
            try:
                # Copy into new folder
                masked_folder_contents = [os.path.join(masked_folder_dir, '{}_{}.{}'.format(new_filename, num, 'mp4')) for num in range(1, len(original_folder_contents)+1)]
                for orig_file, masked_file in zip(original_folder_contents, masked_folder_contents):

                    shutil.copyfile(orig_file, masked_file)
                    reviewer_file_keys[file] = masked_file
                    master_file_keys[file] = {'reviewer': reviewer_value, 'mask': new_filename}

                write_dict_to_csv(reviewer_file_keys_save_path, reviewer_file_keys)
            except:
                print('Check your file paths?')
                write_dict_to_csv(reviewer_file_keys_save_path, reviewer_file_keys)
                write_dict_to_csv(master_file_keys_save_path, master_file_keys)
                return master_file_keys

    try:
        write_dict_to_csv(master_file_keys_save_path, master_file_keys)
    except:
        print('couldnt save master key file')
        return False
    return True