import unittest
import os
import shutil
import blinded.Blinded as bd
import random
from pathlib import Path


class Reviewer:
    def __init__(self, reviewer, blind_dir):
        self.name = reviewer
        self.value = reviewer[0]+reviewer[-1]
        self.dir = os.path.join(os.path.join(blind_dir, '_'.join(reviewer.split(' '))))
        self.toScore = os.path.join(self.dir, 'toScore_' + self.value)
        self.scored = os.path.join(self.dir, 'Scored_' + self.value)
        self.keys_path = os.path.join(blind_dir, '.mask_keys', 'mask_' + self.value + '.csv')


def set_up_blind_dir(blind_dir, reviewers):
    Path(blind_dir).mkdir()
    for reviewer in reviewers:
        this_reviewer = Reviewer(reviewer, blind_dir)
        Path(this_reviewer.toScore).mkdir(parents=True)
        Path(this_reviewer.scored).mkdir()


def set_up_data_dir(data_dir, subjects):
    os.mkdir(data_dir)
    for subject in subjects:
        mouse_dir = os.path.join(data_dir, 'et{}/'.format(subject))
        for session_folder in range(1, 22):
            session_folder_dir = os.path.join(mouse_dir, 'Training', 'et{}_T{}'.format(subject, session_folder))

            for review_folder in range(1, 4):

                review_folder_dir = os.path.join(session_folder_dir, 'Reaches0' + str(review_folder))
                Path(review_folder_dir).mkdir(parents=True)

                review_file = os.path.join(session_folder_dir, 'subject_date_folder_{}.csv'.format(review_folder))
                Path(review_file).touch()
                for file_num in range(1, 21):
                    test_data_file = os.path.join(review_folder_dir, 'test_data_file_' + str(file_num) + '.txt')
                    Path(test_data_file).touch()


def set_up_add_previously_masked_files(data_dir, blind_dir, reviewers):
    subjects = bd.get_subjects(data_dir)
    [_, not_reviewed_files] = bd.get_all_files_review_status(data_dir)
    files_to_mask = []
    for subj in subjects:
        for T in range(1, 4):
            file = [item for item in not_reviewed_files if item.endswith(f'{subj}/Training/{subj}_T{T}/subject_date_folder_1.csv')]
            files_to_mask.append(file[0])
    bd.mask_files(blind_dir, files_to_mask, reviewers)


class BlindDirectorySetUpTestCase(unittest.TestCase):
    blinded_dir = bd.__file__
    blinded_dir = os.path.dirname(blinded_dir)
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')

    def setUp(self):
        self.reviewers = {'Reviewer 1', 'Reviewer 2', 'Reviewer 3'}
        set_up_blind_dir(self.test_blind_dir, self.reviewers)

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)

    def test_get_current_reviewers(self):
        reviewers = bd.get_current_reviewers(self.test_blind_dir)
        self.assertSetEqual(reviewers, self.reviewers)

        for reviewer in reviewers:
            this_reviewer = Reviewer(reviewer, self.test_blind_dir)
            self.assertTrue(os.path.exists(this_reviewer.toScore))
            self.assertTrue(os.path.exists(this_reviewer.scored))


class FullDirectorySetUpTestCase(unittest.TestCase):
    blinded_dir = bd.__file__
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')
    test_data_dir = os.path.join(os.path.dirname(blinded_dir), '.test_data')

    def setUp(self):
        self.reviewers = {'Tom H', 'Dick C', 'Harry P'}
        self.subjects = {'7061', '743'}

        set_up_blind_dir(self.test_blind_dir, self.reviewers)
        set_up_data_dir(self.test_data_dir, self.subjects)

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_get_all_files_review_status(self):
        [reviewed_files, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        self.assertEqual(len(reviewed_files), 0)
        self.assertEqual(len(not_reviewed_files), len(self.subjects)*63)

    def test_get_all_masked_files(self):
        [master_file_keys, file_mask_keys, all_masked_files_by_reviewer] = bd.get_all_masked_files(self.test_blind_dir)
        self.assertTrue(len(master_file_keys) == 0)
        self.assertTrue(len(file_mask_keys) == 0)
        self.assertTrue(len(all_masked_files_by_reviewer) == 0)

    def test_mask_files_no_existing_masks(self):
        master_file_key_path = os.path.join(self.test_blind_dir, '.mask_keys', 'master_file_keys.csv')
        reviewers = bd.get_current_reviewers(self.test_blind_dir)
        [_, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        bd.mask_files(self.test_blind_dir, not_reviewed_files, reviewers)
        self.assertTrue(os.path.exists(master_file_key_path))
        for reviewer in reviewers:
            this_reviewer = Reviewer(reviewer, self.test_blind_dir)
            self.assertTrue(os.path.exists(this_reviewer.keys_path))


class AddNewMaskedFilesTestCase(unittest.TestCase):
    blinded_dir = bd.__file__
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')
    test_data_dir = os.path.join(os.path.dirname(blinded_dir), '.test_data')

    def setUp(self):
        self.reviewers = {'Tom H', 'Dick C', 'Harry P'}
        self.subjects = {'7061', '743'}

        set_up_blind_dir(self.test_blind_dir, self.reviewers)
        set_up_data_dir(self.test_data_dir, self.subjects)
        set_up_add_previously_masked_files(self.test_data_dir, self.test_blind_dir, self.reviewers)

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_get_all_masked_files(self):
        [master_file_keys, file_mask_keys, all_masked_files_by_reviewer] = bd.get_all_masked_files(self.test_blind_dir)
        self.assertTrue(len(master_file_keys) == 120)
        self.assertTrue(len(file_mask_keys) == 6)
        self.assertTrue(len(all_masked_files_by_reviewer) == 3)

    def test_get_all_files_review_status(self):
        [reviewed_files, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        default_reviewed_files = 3*len(self.subjects)
        self.assertEqual(len(reviewed_files), default_reviewed_files)
        self.assertEqual(len(not_reviewed_files), len(self.subjects) * 63 - default_reviewed_files)

    def test_add_new_masked_files(self):
        master_file_key_path = os.path.join(self.test_blind_dir, '.mask_keys', 'master_file_keys.csv')
        [_, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        files_to_mask = random.sample(not_reviewed_files, 15)
        bd.mask_files(self.test_blind_dir, files_to_mask, self.reviewers)

        [_, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        self.assertTrue(os.path.exists(master_file_key_path))
        total_masked_folders = 0
        for reviewer in self.reviewers:
            this_reviewer = Reviewer(reviewer, self.test_blind_dir)
            total_masked_folders += len(os.listdir(this_reviewer.toScore))
            self.assertTrue(this_reviewer.keys_path)
        self.assertEqual(total_masked_folders, 15)
