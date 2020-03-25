# %%
import os
import platform
import re

sharedx_animal_dir = 'Neuro-Leventhal/data/mouseSkilledReaching/'
scorers = set(['AB', 'AC', 'DL', 'JM', 'KF', 'KK'])

# %%
OPERATING_SYSTEM = platform.platform()

## Update this section as you run the code on other computers
if 'Windows' in OPERATING_SYSTEM:
    animals_base_dir = 'X:/' + sharedx_animal_dir
elif ('Debian' in OPERATING_SYSTEM) or ('Darwin' in OPERATING_SYSTEM):
    animals_base_dir = '/Volumes/SharedX/' + sharedx_animal_dir
else:
    animals_base_dir = input(
        'Please provide the FULL PATH for the directory containing all data, organized by animal: ')

et_files = [entry for entry in os.listdir(animals_base_dir) if entry.startswith('et')]

# %%

csv_files_frames = []
csv_files_scored = []

for etdir in et_files:

    eartag = etdir.strip('et')
    et_dir = animals_base_dir + etdir
    et_training_dir = et_dir + '/Training/'

    if not os.path.isdir(et_training_dir):
        continue
    if eartag == '7081':
        continue

    for item in os.listdir(et_training_dir):
        trainingday_dir = et_training_dir + item + '/'

        if not os.path.isdir(trainingday_dir):
            continue

        these_csv_files = [trainingday_dir + file for file in os.listdir(trainingday_dir) if file.endswith('.csv')]

        for file in these_csv_files:
            test_string = file.split('/')[-1]
            if re.search('\S+_\S+_\S+_\S+_\S+.csv', test_string):
                csv_files_scored.append(file)
                continue
            csv_files_frames.append(file)

# %%

scored_files_dict = dict()

for scored_file in csv_files_scored:
    dictKey = scored_file[:-7]
    fileID = scored_file.split('/')[-1]
    fileID = fileID.strip('.csv')
    fileID = fileID.split('_')
    scorer = fileID[-1]
    if dictKey in scored_files_dict.keys():
        existing_scorers = scored_files_dict[dictKey]
        existing_scorers.append(scorer)
        scored_files_dict[dictKey] = existing_scorers
    else:
        scored_files_dict[dictKey] = [scorer]

# %%

files_scored_by_everyone = [elt for elt in scored_files_dict.keys() if len(scored_files_dict[elt]) == 3]

# %%

for file in files_scored_by_everyone:

    # Open each of the csv files associated with this video
    trainingday_dir = '/'.join(file.split('/')[:-1])
    fileID = file.split('/')[-1]

    these_csv_files = []
    for training_file in os.listdir(trainingday_dir):
        if training_file == fileID + '.csv':
            continue
        if training_file.startswith(fileID) and training_file.endswith('.csv'):
            these_csv_files.append(training_file)

    for scored_csv in these_csv_files:
        full_path_scored_csv = trainingday_dir + '/' + scored_csv
        with open(full_path_scored_csv) as F:



