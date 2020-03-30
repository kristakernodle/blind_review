import random
import blinded.Blinded as Bd


blind_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring'
data_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching'
reviewers = {'Dan L', 'Jen M', 'Alli C', 'Kenny F', 'Krista K'}

[reviewed_files, not_reviewed_files] = Bd.get_all_files_review_status(data_dir)
files_to_mask = random.sample(not_reviewed_files, 30)
Bd.mask_files(blind_dir, files_to_mask, reviewers)
