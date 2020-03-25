#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 10:32:33 2019

@author: kkrista
"""
import os
import csv
import shutil
from functions_blindedScoring import randFilenameGen

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

AB_maskedFilename = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_C/masked_AC.csv'
AB_untranslatedDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_C/unTranslated_AC/'
AB_translatedDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_C/toScore/'

stillCutting = '7062_20190827_CC2_03'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)
maskDict = []
originalNames = []
maskedNames = []

# Get all untranslated files
AB_untranslated = os.listdir(AB_untranslatedDir)
AB_untranslated = [item for item in AB_untranslated if item.endswith('.csv')]
for item in AB_untranslated:
    newItem = item.split('_')
    newItem = '_'.join(newItem[:-1])
    AB_untranslated[AB_untranslated.index(item)] = newItem
    
with open(AB_maskedFilename, mode='r') as fin:
    rd = csv.DictReader(fin)
    for row in rd:
        originalNames.append(row['Original Name'])
        maskedNames.append(row['New Name'])
        maskDict.append({'Original Name':row['Original Name'],'New Name':row['New Name']})

# Get all animal folders
for file in allFolders:
    if 'et' in file[:2]:
        # Collect the files that have 'et', denoting 'Ear Tag' into one list
        allAnimals.append(file)
allAnimals.sort()

for animal in allAnimals:
    
    # Define training directory for animal
    currAnDir=animalDir+animal+'/Training/'
        
    if not os.path.isdir(currAnDir):
        # If there is no 'Training' directory, skip this animal
        continue
    
    # Get contents of 'Training' directory
    allTrainDays=os.listdir(currAnDir)
    allTrainDays.sort()
    
    # Loop through training days
    for day in allTrainDays:

        if ('.MP4' in day):
            # Skip .MP4 files in 'Training' directory
            continue

        # Define training day directory
        currDayDir=currAnDir+day

        if not os.path.isdir(currDayDir):
            # Skip 'Training/*' items that are not directories
            continue

        # Identify where we're at in the code, in case of issues
        print('Checking: ' + day)

        # Get all contents of the training day directory
        allFiles=os.listdir(currDayDir)
        
        # Get existing reach directories
        existingReachDir=[file for file in allFiles if 'Reaches' in file]
        
        # If no reach directories exist, move to the next training day
        if len(existingReachDir) == 0:
            continue
        
        # Create names to check against untranslated files
        vidID = day.strip('et')
        vidID = vidID.split('_')
        vidID = '_'.join(vidID[:-1])
        
        for item in existingReachDir:
            vidNum = item.strip('Reaches')
            dayOrigVidName = ('_'.join([vidID,vidNum]))
            
            # Check if the dayOrigVidName is in the untranslated files
            if dayOrigVidName in AB_untranslated or dayOrigVidName in originalNames:
                continue
            else:
                print('Translating Videos: ' + dayOrigVidName)
                
                newName = randFilenameGen()
                
                while newName in maskedNames:
                    newName = randFilenameGen()
                    
                originalNames.append(dayOrigVidName)
                maskedNames.append(newName)
                
                maskDict.append({'Original Name':dayOrigVidName,'New Name':newName})
                
                reachDir = currDayDir + '/' + item + '/'
                
                allReaches = os.listdir(reachDir)
                allReaches = [video for video in allReaches if video.endswith('.mp4')]
                
                for reach in allReaches:
                    
                    if not os.path.isdir(AB_translatedDir + newName):
                        os.mkdir(AB_translatedDir + newName)
                    
                    reachID = reach.split('_')[-1]
                    
                    oldFile = reachDir + reach
                    newFile = AB_translatedDir + newName + '/' + '_'.join([newName,reachID])
                    try:
                        shutil.copy(oldFile, newFile)
                    except:
                        continue
                                
csv_columns = ['Original Name','New Name']
with open(AB_maskedFilename, 'w') as f:
    writer = csv.DictWriter(f,fieldnames=csv_columns)
    writer.writeheader()
    for data in maskDict:
        writer.writerow(data)
                
            
                
                
                
                
            
            
            
            


























