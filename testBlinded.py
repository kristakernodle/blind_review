import unittest
import os
import shutil
import Blinded as bd
import random
from pathlib import Path


class TDHTestCase(unittest.TestCase):
    blinded_dir = bd.__file__
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')
    test_data_dir = os.path.join(os.path.dirname(blinded_dir), '.test_data')

    def setUp(self):
        reviewers = {'Tom_H', 'Dick_C', 'Harry_P'}
        mice = {'7061', '743'}

        # Set Up Blind Directory
        os.mkdir(self.test_blind_dir)
        for reviewer in reviewers:
            os.mkdir( os.path.join(os.path.join(self.test_blind_dir, reviewer)) )

        # Set Up Data Directory
        os.mkdir(self.test_data_dir)
        for mouse in mice:
            mouse_dir = os.path.join(self.test_data_dir, 'et{}/'.format(mouse))
            for session_folder in range(1, 22):
                session_folder_dir = os.path.join(mouse_dir, 'Training', 'et{}_T{}'.format(mouse, session_folder))

                for review_folder in range(1, 4):

                    review_folder_dir = os.path.join(session_folder_dir, 'Reaches0'+str(review_folder))
                    Path(review_folder_dir).mkdir(parents=True)

                    for file_num in range(1, 21):
                        test_data_file = os.path.join(review_folder_dir, 'test_data_file_' + str(file_num) + '.txt')
                        Path(test_data_file).touch()

                    if session_folder % 2 == 0:
                        review_file = os.path.join(session_folder_dir, 'subject_date_folder_{}.csv'.format(review_folder))
                    else:
                        reviewer = random.sample(reviewers, 1)[0]
                        reviewer_value = '_' + reviewer[0] + reviewer[-1]
                        review_file = os.path.join(session_folder_dir, 'subject_date_folder_{}_{}.csv'.format(review_folder, reviewer_value))
                    Path(review_file).touch()

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_get_current_reviewers(self):
        reviewers = bd.get_current_reviewers(self.test_blind_dir)
        self.assertSetEqual(reviewers, {'Dick C', 'Harry P', 'Tom H'})

    def test_get_all_files_review_status(self):
        [reviewed_files, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        self.assertEqual(len(reviewed_files), 66)
        self.assertEqual(len(not_reviewed_files), 60)

    def test_mask_files(self):
        master_file_key_path = os.path.join(self.test_blind_dir, '.mask_keys', 'master_file_keys.csv')
        reviewers = bd.get_current_reviewers(self.test_blind_dir)
        [_, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        bd.mask_files(self.test_blind_dir, not_reviewed_files, reviewers)
        self.assertTrue(os.path.exists(master_file_key_path))
        for reviewer in reviewers:
            reviewer_value = reviewer[0]+reviewer[-1]
            reviewer_file_keys_path = os.path.join(self.test_blind_dir, '.mask_keys', 'mask_' + reviewer_value + '.csv')
            self.assertTrue(os.path.exists(reviewer_file_keys_path))




