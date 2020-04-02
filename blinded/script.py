import random

import blinded.blinddir.masks as ms
import blinded.blinddir.reviewers as rs


blind_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring'
data_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching'
reviewers = {'Dan L'}

[reviewed_files, not_reviewed_files] = rs.get_all_files_review_status(data_dir)
files_to_mask = random.sample(not_reviewed_files, 40)
ret = ms.mask_files(blind_dir, files_to_mask, reviewers)

if len(ret) > 4:
    print('hello')