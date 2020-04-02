import os
import random
import shutil
import unittest

from . import set_up_functions as sf
from ..blinddir.masks import get_all_masked_files, mask_files
from ..blinddir.reviewers import get_current_reviewers, get_all_files_review_status
from ..common.classproperty import Reviewer


class BlindDirDataDirSetUpTestCase(unittest.TestCase):
    blinded_dir = __file__
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')
    test_data_dir = os.path.join(os.path.dirname(blinded_dir), '.test_data')

    def setUp(self):
        self.reviewers = {'Tom H', 'Dick C', 'Harry P'}
        self.subjects = {'7061', '743'}

        sf.set_up_blind_dir(self.test_blind_dir, self.reviewers)
        sf.set_up_data_dir(self.test_data_dir, self.subjects)

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_get_all_masked_files(self):
        [master_file_keys, file_mask_keys, all_masked_files_by_reviewer] = get_all_masked_files(self.test_blind_dir)
        self.assertTrue(len(master_file_keys) == 0)
        self.assertTrue(len(file_mask_keys) == 0)
        self.assertTrue(len(all_masked_files_by_reviewer) == 0)

    def test_mask_files_no_existing_masks(self):
        master_file_key_path = os.path.join(self.test_blind_dir, '.mask_keys', 'master_file_keys.csv')
        reviewers = get_current_reviewers(self.test_blind_dir)
        [_, not_reviewed_files] = get_all_files_review_status(self.test_data_dir)
        mask_files(self.test_blind_dir, not_reviewed_files, reviewers)
        self.assertTrue(os.path.exists(master_file_key_path))
        for reviewer in reviewers:
            this_reviewer = Reviewer(reviewer, self.test_blind_dir)
            self.assertTrue(os.path.exists(this_reviewer.keys_path))


class PreviouslyMaskedFilesTestCase(unittest.TestCase):
    blinded_dir = __file__
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')
    test_data_dir = os.path.join(os.path.dirname(blinded_dir), '.test_data')

    def setUp(self):
        self.reviewers = {'Tom H', 'Dick C', 'Harry P'}
        self.subjects = {'7061', '743'}

        sf.set_up_blind_dir(self.test_blind_dir, self.reviewers)
        sf.set_up_data_dir(self.test_data_dir, self.subjects)
        sf.set_up_add_previously_masked_files(self.test_data_dir, self.test_blind_dir, self.reviewers)

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_get_all_masked_files(self):
        [master_file_keys, file_mask_keys, all_masked_files_by_reviewer] = get_all_masked_files(self.test_blind_dir)
        self.assertTrue(len(master_file_keys) == 6)
        self.assertTrue(len(file_mask_keys) == 6)
        self.assertTrue(len(all_masked_files_by_reviewer) == len(self.reviewers))

    def test_add_new_masked_files(self):
        [master_file_keys, _, _] = get_all_masked_files(self.test_blind_dir)
        [_, not_reviewed_files] = get_all_files_review_status(self.test_data_dir)
        not_reviewed_files = set(not_reviewed_files)
        master_file_keys = set(list(master_file_keys.keys()))
        files_to_mask = random.sample(not_reviewed_files.difference(master_file_keys), 15)
        mask_files(self.test_blind_dir, files_to_mask, self.reviewers)
        [master_file_keys, file_mask_keys, all_masked_files_by_reviewer] = get_all_masked_files(self.test_blind_dir)
        self.assertTrue(len(all_masked_files_by_reviewer) == len(self.reviewers))
        self.assertTrue(len(master_file_keys) == len(file_mask_keys) == 21)
