from unittest import TestCase
import os
import shutil

from . import set_up_functions as sf
from ..blinddir.reviewers import get_current_reviewers, get_all_files_review_status
from ..common.classproperty import Reviewer


class NoReviewedFilesTestCase(TestCase):
    blinded_dir = __file__
    blinded_dir = os.path.dirname(blinded_dir)
    blind_dir = os.path.join(os.path.dirname(blinded_dir), 'tests', '.test_blind_dir')
    data_dir = os.path.join(os.path.dirname(blinded_dir), 'tests', '.test_data_dir')

    def setUpClass(self):
        self.reviewers = {'Reviewer 1', 'Reviewer 2', 'Reviewer 3'}
        self.subjects = {'7061', '743'}
        sf.set_up_blind_dir(self.blind_dir, self.reviewers)
        sf.set_up_data_dir(self.data_dir, self.subjects)

    def tearDownClass(self):
        shutil.rmtree(self.blind_dir, ignore_errors=True)

    def test_get_current_reviewers(self):
        reviewers = get_current_reviewers(self.blind_dir)
        self.assertSetEqual(reviewers, self.reviewers)

        for reviewer in reviewers:
            this_reviewer = Reviewer(reviewer, self.blind_dir)
            self.assertTrue(os.path.exists(this_reviewer.toScore))
            self.assertTrue(os.path.exists(this_reviewer.scored))

    def test_get_all_files_review_status(self):
        [reviewed_files, not_reviewed_files] = get_all_files_review_status(self.data_dir)
        self.assertEqual(len(reviewed_files), 0)
        self.assertEqual(len(not_reviewed_files), len(self.subjects)*63)
