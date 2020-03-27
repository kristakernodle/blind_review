import unittest
import os
import shutil
import Blinded as bd


class TDHTestCase(unittest.TestCase):
    blinded_dir = bd.__file__
    test_blind_dir = os.path.join(os.path.dirname(blinded_dir), '.test_blind_dir')

    def setUp(self):
        reviewers = {'Tom_H', 'Dick_C', 'Harry_P'}
        os.mkdir(self.test_blind_dir)
        for reviewer in reviewers:
            os.mkdir( os.path.join(os.path.join(self.test_blind_dir, reviewer)) )

    def tearDown(self):
        shutil.rmtree(self.test_blind_dir, ignore_errors=True)

    def test_get_current_reviewers(self):
        reviewers = bd.get_current_reviewers(self.test_blind_dir)
        self.assertSetEqual(reviewers, {'Tom_H', 'Dick_C', 'Harry_P'})

