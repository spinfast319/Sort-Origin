# Sort Albums with Origin Files
# author: hypermodifiede
# This script is meant to use yaml origin files and track metadata to sort the albums into different directories so they can be processed later
# It has been tested and works in both Ubuntu Linux and Windows 10.

# Before running this script install the dependencies

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import yaml  # Imports yaml
import shutil  # Imports functionality that lets you copy files and directory
import datetime  # Imports functionality that lets you make timestamps

#  Set your directories here
album_directory = "M:\Python Test Environment\Albums"  # Which directory do you want to start with?
renamed_directory = "M:\Python Test Environment\Renamed"  # Which directory do you want to copy the rename folders to?
log_directory = "M:\Python Test Environment\Logs"  # Which directory do you want the log in?
work_directory = "M:\Python Test Environment\Work"  # Create directory for temp file storage and renaming


# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 1

# Establishes the counters for completed albums and missing origin files
count = 0
good_missing = 0
bad_missing = 0
parse_error = 0
error_message = 0

# identifies location origin files are supposed to be
path_segments = album_directory.split(os.sep)
segments = len(path_segments)
origin_location = segments + album_depth

# A function to log events
def log_outcomes(directory, log_name, message):
    global log_directory

    script_name = "Sort Albums with Origin Files Script"
    today = datetime.datetime.now()
    log_name = f"{log_name}.txt"
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    log_path = os.path.join(log_directory, log_name)
    with open(log_path, "a", encoding="utf-8") as log_name:
        log_name.write(f"--{today:%b, %d %Y} at {today:%H:%M:%S} from the {script_name}.\n")
        log_name.write(f"The album folder {album_name} {album_name}.\n")
        log_name.write(f"Album location: {directory}\n")
        log_name.write(" \n")
        log_name.close()


# The main function that controls the flow of the script
def main():

    try:
        # intro text
        print("")
        print("Do or do not...")

        # Run the function to loop through the list.txt file and rehost the cover art
        # sort_albums()

    finally:
        # Summary text
        print("")
        print("There is no try...")
        # run summary text function to provide error messages
        # summary_text()
        print("")


if __name__ == "__main__":
    main()
