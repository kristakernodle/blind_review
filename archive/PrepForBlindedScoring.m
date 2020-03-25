%% Prep for Blinded Scoring
% Version 1, 20190107
% Author: Krista Kernodle (kkrista@umich.edu)
%
% Purpose: This code translates filenames into a new, randomly generated 10
%   digit filename. Uniqueness is checked both for the original file name
%   (so a file will not be translated twice) and for the randomly generated
%   filename (to eliminate difficulties in unblinding for analysis). 
%
% Inputs: 
%
%   transDir - Directory of the .mat file containing translated names and
%       original names
%   transName - name of the .mat file containing translated names and
%       original names
%   inDir - Directory of all files that need renaming
%   inDirWant - Common aspect of all folder names in the inDir
%   subDir - Commonly named folder for all folders in the inDir
%   subDirWant - Common aspect of all folder names in the subDir
%   finFoldWant - Common aspect of all folder names that contain files to
%       be renamed
%   filenameStruct - Commonly formatted names of all files to be renamed
%   outDir - Directory all renamed files will be copied to
%
%   NOTE: This code assumes that a .mat file already exists.  
%
% Outputs:
%   All copied files (located in outDir)
%   Updated .mat file with all original and new filenames
%

%% Inputs
transDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_B/';
transName = 'translated_AB.mat';
inDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/';
inDirWant = 'et';
subDir = '/Training/';
subDirWant = 'CC';
finFoldWant = 'Reaches';
filenameStruct = '/*_*_*_*_*.MP4';
outDir = '/Volumes/KRISTAEHD/Scoring_AlliB/';

%% Initiate Variables
wantFolders = [];
allNewNames = [];
uniqOrigNames = [];

%% Import .mat

transFile = load([transDir,transName]);
allOrigName = transFile.allOrigName;
allNewName = transFile.allNewName;

%% First Level of Folders
% wantFolders

files = dir(inDir);
dirFlags1 = [files.isdir];
subFolders = files(dirFlags1);

% Get only the folders of the inDir that containe inDirWant
for ii = 1:length(subFolders)
    
    currFold = subFolders(ii).name;
    
    if contains(currFold,inDirWant)
        wantFolders = [wantFolders; string(currFold)];
    end
    
end

%% Second Level of Folders
% wantTrainFolders

for jj = 1:length(wantFolders)
   
    animal = char(wantFolders(jj));
    trainDir = strcat(inDir, animal, subDir);
    trainFiles = dir(trainDir);
    dirFlags2 = [trainFiles.isdir];
    subTrainFolders = trainFiles(dirFlags2);
    
    wantTrainFolders = [];
    
    for jk = 1:length(subTrainFolders)
        
       currTrainFold = subTrainFolders(jk).name;
        
       if contains(currTrainFold,subDirWant)
           wantTrainFolders = [wantTrainFolders; string(currTrainFold)];
       end
        
    end
    
    %% Third Level of Folders
    % wantReachFolders
    
    for jl = 1:length(wantTrainFolders)
        
        trainDay = char(wantTrainFolders(jl));
        reachDir = strcat(trainDir,trainDay);
        reachFiles = dir(reachDir);
        dirFlags3 = [reachFiles.isdir];
        subReachFolders = reachFiles(dirFlags3);
        
        wantReachFolders = [];
        
        for jlm = 1:length(subReachFolders)
            
            currReach = subReachFolders(jlm).name;
            
            if contains(currReach,finFoldWant)
                wantReachFolders = [wantReachFolders; string(currReach)];
            end
        end
        
        %% Get all files in reachDir that can be translated
        % origName
        
        for jln = 1:length(wantReachFolders)
            allFiles = dir(strcat(reachDir,'/',char(wantReachFolders(jln)),filenameStruct));
            if isempty(allFiles)
                continue
            end
            firstName = allFiles(1).name;
            split = strsplit(firstName,'_');
            
            % Dunno why, but some files will have a ._ in front, this is my
            % solution to get the original name without the ._
            if length(split) == 4
                origName = strcat(split{1},'_',split{2},'_',split{3},'.MP4');
            elseif length(split) == 5
                origName = strcat(split{2},'_',split{3},'_',split{4},'.MP4');
            else
                disp(length(split));
            end
            
            %% Generate New Names
            
            % Check for uniqueness of origName (not previously translated)
            if ~any(strcmp(origName,allOrigName))
                
                % For unique origName, generate newName
                newName = randFilenameGen();
                
                % Check uniqueness of newName
                while (any(strcmp(newName,allNewName))) || (strcmp(newName,allNewNames))
                    disp('in loop');
                    newName = randFilenameGen();
                end
                
                %% Begin Translation
                
                % Save all newly generated names in character array allNewNames 
                allNewNames = [allNewNames;newName];
                
                % Save all unique origName in character array uniqOrigNames
                uniqOrigNames = [uniqOrigNames;origName];
                
            else
                % If not unique, continue to next file
                continue
            end % Check Uniqueness (Generate New Names)
            
            %% Change Filename and Move File
            
            % First create the new folder, if necessary.
            outputFolder = fullfile(outDir,newName);
            if ~exist(outputFolder, 'dir')
              mkdir(outputFolder);
            end
            
            % Copy the files over with a new name.
            fileNames = { allFiles.name };
            for jlni = 1 : length(allFiles)
              thisFileName = fileNames{jlni};
              split2 = strsplit(thisFileName,'_');
              % Prepare the input filename.
              inputFullFileName = strcat(reachDir,'/',char(wantReachFolders(jln)),'/',thisFileName);
              % Prepare the output filename.
              outputBaseFileName = sprintf('%s_%s', newName, string(split2(end)));
              outputFullFileName = fullfile(outputFolder, outputBaseFileName);
              % Do the copying and renaming all at once.
              copyfile(inputFullFileName, outputFullFileName);
            end
            
  
        end % Get all files in reachDir that can be translated
        
    end % Third level of folders

end % Second level of folders

%% Save All

% % Convert character arrays uniqOrigNames & allNewNames to strings
uniqOrigNames = string(uniqOrigNames);
allNewNames = string(allNewNames);
allOrigName = string(allOrigName);
allNewName = string(allNewName);
% 
% % Concatenate into one variable (transFile)
startRowCt = size(allOrigName,1)+1;
endRowCt = size(allOrigName,1)+length(uniqOrigNames);
allOrigName(1:startRowCt-1,1) = allOrigName;
allOrigName(startRowCt:endRowCt,1) = uniqOrigNames;
allNewName(1:startRowCt-1,1) = allNewName;
allNewName(startRowCt:endRowCt,1) = allNewNames;
% 
% % Save new transFile as .mat, overwritting old variables
% 
% 
% save '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_B/translated_AB.mat' allOrigName allNewName
% 
% 



















