#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functions_blinded as blind


data_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'
blind_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/'

[reviewed_files, not_reviewed_files] = blind.get_all_files_review_status(data_dir)