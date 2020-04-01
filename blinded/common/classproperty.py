import os

from ..blinddir import reviewers as rv
from ..blinddir import masks as mk


class Reviewer:
    def __init__(self, reviewer, blind_dir):
        self.name = reviewer
        self.value = reviewer[0]+reviewer[-1]
        self.dir = os.path.join(os.path.join(blind_dir, '_'.join(reviewer.split(' '))))
        self.toScore = os.path.join(self.dir, 'toScore_' + self.value)
        self.scored = os.path.join(self.dir, 'Scored_' + self.value)
        self.keys_path = os.path.join(blind_dir, '.mask_keys', 'mask_' + self.value + '.csv')

    def get_assigned_files(self, data_dir, blind_dir):
        [reviewed_files, _] = rv.get_all_files_review_status(data_dir)
        [_, _, all_masked_files_by_reviewer] = mk.get_all_masked_files(blind_dir)

        assigned_files = all_masked_files_by_reviewer[self.value]

        for file in reviewed_files:
            filename_wo_ext = os.path.splitext(file)[0]
            reviewer_value = filename_wo_ext[-2:]
            if reviewer_value == self.value:
                assigned_files.append(file)
        return assigned_files
