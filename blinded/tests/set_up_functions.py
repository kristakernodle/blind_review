from pathlib import Path
import os

from ..common.classproperty import Reviewer
from ..common.auxiliary_functions import get_subjects
from ..blinddir.reviewers import get_current_reviewers, get_all_files_review_status
from ..blinddir.masks import mask_files


def set_up_blind_dir(blind_dir, reviewers):
    Path(blind_dir).mkdir()
    for reviewer in reviewers:
        this_reviewer = Reviewer(reviewer, blind_dir)
        Path(this_reviewer.toScore).mkdir(parents=True)
        Path(this_reviewer.scored).mkdir()


def set_up_data_dir(data_dir, subjects):
    os.mkdir(data_dir)
    for subject in subjects:
        subj_dir = os.path.join(data_dir, 'et{}/'.format(subject))
        for session_folder in range(1, 22):
            session_folder_dir = os.path.join(subj_dir, 'Training', 'et{}_T{}'.format(subject, session_folder))

            for review_folder in range(1, 4):

                review_folder_dir = os.path.join(session_folder_dir, 'Reaches0' + str(review_folder))
                Path(review_folder_dir).mkdir(parents=True)

                review_file = os.path.join(session_folder_dir, 'subject_date_folder_{}.csv'.format(review_folder))
                Path(review_file).touch()

                for file_num in range(1, 21):
                    test_data_file = os.path.join(review_folder_dir, 'test_data_file_' + str(file_num) + '.txt')
                    Path(test_data_file).touch()


def set_up_add_previously_masked_files(data_dir, blind_dir, reviewers):
    subjects = get_subjects(data_dir)
    [_, not_reviewed_files] = get_all_files_review_status(data_dir)
    files_to_mask = []
    for subj in subjects:
        subj = 'et' + subj
        for T in range(1, 4):
            file = [item for item in not_reviewed_files if item.endswith(f'{subj}/Training/{subj}_T{T}/subject_date_folder_1.csv')]
            files_to_mask.append(file[0])
    mask_files(blind_dir, files_to_mask, reviewers)


def set_up_add_previously_reviewed_files(data_dir, blind_dir):
    subjects = get_subjects(data_dir)
    reviewers = get_current_reviewers(blind_dir)
    reviewer = reviewers.pop()
    reviewer_value = reviewer[0]+reviewer[-1]
    for subject in subjects:
        subj_dir = os.path.join(data_dir, 'et{}/'.format(subject))
        for session_folder in range(1, 22):
            session_folder_dir = os.path.join(subj_dir, 'Training', 'et{}_T{}'.format(subject, session_folder))
            reviewed_file = os.path.join(session_folder_dir, 'subject_date_folder_1_{}.csv'.format(reviewer_value))
            Path(reviewed_file).touch()
