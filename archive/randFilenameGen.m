function randName = randFilenameGen()

%% Random Filename Generator
% The purpose of this file is to create a random filename that
% contains lowercase letters and numbers. 
% 
% Inputs: 
%       None
%
% Outputs:
%       randName - a string array consisting of the randomly generated
%       filename


% Array containing all possible elements in the filenames
el = {'a','b','c','d','e','f','g','h','i','j','k','l','m',...
            'n','o','p','q','r','s','t','u','v','w','x','y','z',...
            '0','1','2','3','4','5','6','7','8','9'};
        
       
% Generate 10 random integers in [1,36]
randElNum = randi(36,10,1);

% Create a random name based on random numbers (used as indicies
% for el array)
randName = [el{randElNum(1)} el{randElNum(2)} el{randElNum(3)} el{randElNum(4)}...
            el{randElNum(5)} el{randElNum(6)} el{randElNum(7)}...
            el{randElNum(8)} el{randElNum(9)} el{randElNum(10)}];
        

end
        