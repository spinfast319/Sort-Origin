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
log_directory = "M:\Python Test Environment\Logs"  # Which directory do you want the log in?


# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 1

# Establishes the counters for completed albums and missing origin files
count = 0
total_count = 0
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
        log_name.write(f"The album folder {album_name} {message}.\n")
        log_name.write(f"Album location: {directory}\n")
        log_name.write(" \n")
        log_name.close()


# A function that determines if there is an error
def error_exists(error_type):
    global error_message

    if error_type >= 1:
        error_message += 1  # variable will increment if statement is true
        return "Warning"
    else:
        return "Info"


# A function that writes a summary of what the script did at the end of the process
def summary_text():
    global count
    global total_count
    global good_missing
    global bad_missing
    global parse_error
    global error_message

    print("")
    print(f"This script reorganized {count} albums out of {total_count} tried.")
    print("This script looks for potential missing files or errors. The following messages outline whether any were found.")

    error_status = error_exists(parse_error)
    print(f"--{error_status}: There were {parse_error} albums skipped due to not being able to open the yaml. Redownload the yaml file.")
    error_status = error_exists(bad_missing)
    print(f"--{error_status}: There were {bad_missing} folders missing an origin files that should have had them.")
    error_status = error_exists(good_missing)
    print(f"--Info: Some folders didn't have origin files and probably shouldn't have origin files. {good_missing} of these folders were identified.")

    if error_message >= 1:
        print("Check the logs to see which folders had errors and what they were.")
    else:
        print("There were no errors.")


#  A function that gets the directory and then opens the origin file and prints the name of the folder
def get_creators(directory):
    global count
    global good_missing
    global bad_missing
    global parse_error
    global origin_location

    print("\n")
    print(f"Sorting {directory}")
    # check to see if there is an origin file
    file_exists = os.path.exists("origin.yaml")
    # if origin file exists, load it, copy, and rename
    if file_exists == True:
        origin_path = os.path.join(directory, "origin.yaml")
        # open the yaml
        try:
            with open(origin_path, encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)          
        except:
            print("--There was an issue parsing the yaml file and the cover could not be downloaded.")
            print("--Logged missing cover due to parse error. Redownload origin file.")
            log_name = "parse-error"
            log_message = "had an error parsing the yaml and the cover art could not be downloaded. Redownload the origin file"
            log_outcomes(directory, log_name, log_message)
            parse_error += 1  # variable will increment every loop iteration
            return
              
        # turn the data into variables
        creators = {
            "artist_name": data['Artist'],   
            "album_name": data['Name'],
            "dj_name": data['DJs'], 
            "composer_name": data['Composers'],
            "conductor_name": data['Conductors'] 
        }
        f.close()  
        return creators
        
    # otherwise log that the origin file is missing
    else:
        # split the director to make sure that it distinguishes between foldrs that should and shouldn't have origin files
        current_path_segments = directory.split(os.sep)
        current_segments = len(current_path_segments)
        # create different log files depending on whether the origin file is missing somewhere it shouldn't be
        if origin_location != current_segments:
            # log the missing origin file folders that are likely supposed to be missing
            print("--An origin file is missing from a folder that should not have one.")
            print("--Logged missing origin file.")
            log_name = "good-missing-origin"
            log_message = "origin file is missing from a folder that should not have one.\nSince it shouldn't be there it is probably fine but you can double check"
            log_outcomes(directory, log_name, log_message)
            good_missing += 1  # variable will increment every loop iteration
        else:
            # log the missing origin file folders that are not likely supposed to be missing
            print("--An origin file is missing from a folder that should have one.")
            print("--Logged missing origin file.")
            log_name = "bad-missing-origin"
            log_message = "origin file is missing from a folder that should have one"
            log_outcomes(directory, log_name, log_message)
            bad_missing += 1  # variable will increment every loop iteration


# The main function that controls the flow of the script
def main():
    global total_count
    
    try:
        # intro text
        print("")
        print("Do or do not...")

        # Get all the subdirectories of album_directory recursively and store them in a list:
        directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
        directories.remove(os.path.abspath(album_directory))  # If you don't want your main directory included

        #  Run a loop that goes into each directory identified in the list and runs the function that sorts the folders
        for i in directories:
            os.chdir(i)  # Change working Directory
            #check for track and track number data
            creators = get_creators(i)  # Run your function
            print(creators)
            #sort_albums(creators) # Filter out varios artist, dj and classical albums for additional checks
            total_count += 1  # variable will increment every loop iteration

    finally:
        # Summary text
        print("")
        print("There is no try...")
        # run summary text function to provide error messages
        summary_text()
        print("")


if __name__ == "__main__":
    main()
