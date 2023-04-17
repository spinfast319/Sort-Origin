# Sort-Origin
### This is a python script that uses yaml origin files to sort different types of albums into different directories so they can be tagged and renamed later.
Specifically, it identifies and moves albums that have DJ/compiliers instead of artists, classical albums, and Various Artist albums. It moves each of those to a folder of similar types. It leaves the rest of the albums in the directly it is scanning.

It does this so you can automate tagging and renaming of alumbs. If you were to tag and rename the albums it moves you would likely need to handle the way the _artist_ is defined and for some you might want _track number - track name_  and others _track number - artist - track name_. By separating the albums into different folders you can set up different templates and then automate the tagging and renaming of all the albums of a similar type.

It can handle strange characters and nested folders and it logs any errors it runs into. It has been tested and works in both Ubuntu Linux and Windows 10.

This script is meant to work in conjunction with other scripts in order to manage a large music library when the source of the music has good metadata you want to use to organize it.  You can find an overview of the scripts and workflow at [Origin-Music-Management](https://github.com/spinfast319/Origin-Music-Management). 

## Dependencies
This project has a dependency on the gazelle-origin project created by x1ppy. gazelle-origin scrapes gazelle based sites and stores the related music metadata in a yaml file in the music albums folder. For this script to work you need to use a fork that has additional metadata including the tags and coverart. The fork that has the most additional metadata right now is: https://github.com/spinfast319/gazelle-origin

All your albums will need origin files origin files associated with them already for this script to work.

## Install and set up
Clone this script where you want to run it.

Set up or specify the five directories you will be using and specify whether you albums are nested under artist or not.
1. The directory the albums you want to sort and move are in
2. A directory to store the log files the script creates
3. The directory you want Various Artist albums moved to once you sort them
4. The directory you want DJ albums moved to once you sort them
5. The directory you want Classical albums moved to once you sort them
6. Set the album_depth variable to specify whether you are using nested folders or have all albums in one directory
   - If you have all your ablums in one music directory, ie. Music/Album then set this value to 1
   - If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2

The default is 1 (Music/Album)

Use your terminal to navigate to the directory the script is in and run the script from the command line.  When it finishes it will output how many albums it moved.

```
Sort-Origin.py
```

_note: on linux and mac you will likely need to type "python3 Sort-Origin.py"_  
_note 2: you can run the script from anywhere if you provide the full path to it_


When it finishing running the script moves albums of those three types to the directories and leaves the rest in the albums directory. The script will also create logs listing any album that it has problems processing.  
