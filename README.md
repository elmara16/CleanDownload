# CleanDownload

Are you tired of your download folder being in mess? Got bunch of files from questionable sources you need to sort?
Don't worry, there is a solution to your problem.<br>
**The clean python script**
It sorts your movies and shows into a seperate folder, each show has a seperate file for their season

## Functionality

- Sorts movies and series into a seperate folder
- Each series has a seperate folder for each season, but if it's not known which season the file belongs to it's put in the folder called "Unknown"
- Puts the files the program cannot sort into movies or series into the None folder
-

## How to use
1 - Download the newest version of Python if you don't have it already

2 - Get the scrypt

3 - Go to the destination of your folder you want to clean your movies

4 - Rename it to "downloads" if the name of your folder isn't downloads

5 - Go to the command line and run the scrypt by using ./clean.py <br>
 **note:** if it's not executable then type either chmod +x clean.py or chmod 755 clean.py into the command line and then try again

6 - Watch few funny cat videos or get a cofee while waiting for the cleanup to finish

7 - Rename it back to the original name after the script has finished running

## Known Bugs

- Doesn't sort the season/episodes if the name of the file starts on telling which season and episode it is
  <br>**example:** S01E04.How I.Met.Your.Mother.avi 
- Currently only works for Windows
- The search api functionality which was used is not perfect and might not find the show/movie or sort them in the wrong category
- bundles all files together and it might sort pictures into a season if for some reason they were sorted in the series
- Depending on the size of your downloads folder and size of each file the time it takes to sort the files varies and might take rather long to complete
- The folder used must be named 'downloads'
- Cannot move from downloads folder to a different folder while sorting, need to do it manually afterwards if needed
- Not known how far in the file tree the downloads folder can be in because it was only tested to have them in the same folder
