'''

unTranslate is a script designed to unencode any blinded scored files for analysis.

'''

__author__ = "Krista Kernodle"


import os
import shutil


dir_blindscoring_base = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/'
ugrads = {"Alli_B": "AB"}

dir_allanimals = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'
unknown = []

for key in ugrads.keys():
    ugrad_base_dir = os.path.join(dir_blindscoring_base, key)
    ugrad_masked_csv = os.path.join(ugrad_base_dir, 'masked_' + ugrads[key] + '.csv')
    ugrad_scored_dir = os.path.join(ugrad_base_dir, 'Scored_' + ugrads[key])
    ugrad_untranslated_dir = os.path.join(ugrad_base_dir, 'unTranslated_' + ugrads[key])

    all_scored_files = os.listdir(ugrad_scored_dir)
    all_untranslated_files = os.listdir(ugrad_untranslated_dir)

    with open(ugrad_masked_csv) as f:
        ugrad_masked_files = f.read().splitlines()
    for index, line in enumerate(ugrad_masked_files):
        line = line.split(',')
        newline = [line[1], line[0]]
        ugrad_masked_files[index] = newline
    ugrad_masked_files = dict(ugrad_masked_files)

    for scored_file in all_scored_files:
        sf = scored_file
        sf_newname = sf.split('_')[0]

        try:
            sf_origname = ugrad_masked_files[sf_newname]
            savename = sf_origname + '_' + ugrads[key] + '.csv'

            if savename in all_untranslated_files:
                continue
            else:
                origname = sf_origname.split('_')
                initials = ugrads[key]
                shutil.move(os.path.join(ugrad_scored_dir, sf), os.path.join(ugrad_untranslated_dir, savename))
        except KeyError:
            unknown.append(sf)
            continue



'''
Folder Structure:
    - dir_blindedscoring_base / 
        - ugrads[person]
            - masked_UG.csv
            - Scored_UG
                - randfilename_UG.csv
                - ...
            - translated_UG
                - randomname
                    - randomname_01.mp4
                    - randomname_02.mp4 
                    - ...
            - unTranslated_UG
                - animal_file_name_UG.csv
                - ...
            
'''



