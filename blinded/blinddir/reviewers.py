import os
import re


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
            if item.startswith('.'):
                continue
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
    comparison_names = []

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
            current_session_files = sorted(current_session_files, key=len, reverse=True)
            for file in current_session_files:
                if re.search(filename_regex, file):
                    reviewed_files.append(os.path.join(current_session_dir, file))
                    comparison_names.append(file[:-7])
                    continue
                elif file[:-4] in comparison_names:
                    continue
                else:
                    not_reviewed_files.append(os.path.join(current_session_dir, file))

    return reviewed_files, not_reviewed_files

