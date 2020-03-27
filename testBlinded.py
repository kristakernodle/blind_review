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
        # mouse1 = ''

        # Set Up Blind Directory
        os.mkdir(self.test_blind_dir)
        for reviewer in reviewers:
            os.mkdir( os.path.join(os.path.join(self.test_blind_dir, reviewer)) )

        # Set Up Data Directory
        os.mkdir(self.test_data_dir)
        for session_folder in range(1, 22):
            for review_folder in range(1, 4):

                review_folder_dir = os.path.join(self.test_data_dir,
                                                 'et7062/Training/et7062_20190809_CC2_T{}/Reaches0{}'.format(
                                                     session_folder, review_folder))
                Path(review_folder_dir).mkdir(parents=True)
                for i in range(1,21):
                    test_data_file = os.path.join(review_folder_dir, 'test_data_file_' + str(i) + '.txt')
                    Path(test_data_file).touch()
            for i in range(1, 4):
                reviewer = random.sample()
                review_file = os.path.join(self.test_data_dir, 'et7062/Training/et7062_20190809_CC2_T{}'.format(session_folder), 'review_file_'+str(i)+reviewer+'.csv')




    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_get_current_reviewers(self):
        reviewers = bd.get_current_reviewers(self.test_blind_dir)
        self.assertSetEqual(reviewers, {'Dick C', 'Harry P', 'Tom H'})

    def test_get_all_files_review_status(self):
        [reviewed_files, not_reviewed_files] = bd.get_all_files_review_status(self.test_data_dir)
        print(reviewed_files)
        print(not_reviewed_files)




