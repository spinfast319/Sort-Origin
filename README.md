# Sort-Origin
### This is a python script that uses yaml origin files to sort different types of albums into different directories so they can be tagged and renamed later.
Specifically, it identifies and moves albums that have DJ/compiliers instead of artists, classical albums, and Various Artist albums. It moves each of those to a folder of similar types. If you were to tag and rename these you would likely need to handle the way the _artist_ is defined and for some you might want _track number - track name_  and others _track number - artist - track name_. It can handle strange characters and nested folders and it logs any errors it runs into.

It has been tested and works in both Ubuntu Linux and Windows 10.

## Dependencies

This project has a dependency on the gazelle-origin project created by x1ppy. gazelle-origin scrapes gazelle based sites and stores the related music metadata in a yaml file in the music albums folder. It is located here: https://github.com/x1ppy/gazelle-origin

For this script to work you need origin files with additional metadata. The fork that has the most additional metadata right now is: https://github.com/spinfast319/gazelle-origin

All of the albums you want to check will need to have updated origin files created already.

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

Then run the script from the command line.  It moves albums of those three types to the directories and leaves the rest in the albums directory.
