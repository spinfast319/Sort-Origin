# Sort Albums with Origin Files
# author: hypermodified
# This python script is meant to use yaml origin files to sort different types of albums into different directories so they can be tagged and renamed later
# Specifically, it identifies and moves albums that have DJ/compiliers instead of artists, classical albums, and Various Artist albums.
# It moves each of those to a folder of similar types.
# It can handle strange characters and nested folders. It has been tested and works in both Ubuntu Linux and Windows 10.

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import yaml  # Imports yaml
import shutil  # Imports functionality that lets you copy files and directory
import datetime  # Imports functionality that lets you make timestamps

#  Set your directories here
album_directory = "M:\PROCESS"  # Which directory do you want to start with?
log_directory = "M:\PROCESS-LOGS\Logs"  # Which directory do you want the log in?
va_directory = "M:\PROCESS-SORT\Various Artists"  # Directory to move Various Artist albums to
dj_directory = "M:\PROCESS-SORT\DJ"  # Directory to move DJ mix albums to
classical_directory = "M:\PROCESS-SORT\Classical"  # Directory to move classical albums to


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
origin_old = 0

# identifies location origin files are supposed to be
path_segments = album_directory.split(os.sep)
segments = len(path_segments)
origin_location = segments + album_depth

# creates the list of albums that need to be moved post sorting
move_list = []

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
    global origin_old

    print("")
    print(f"This script moved {count} albums out of {total_count} folders examined.")
    print("This script looks for potential missing files or errors. The following messages outline whether any were found.")

    error_status = error_exists(parse_error)
    print(f"--{error_status}: There were {parse_error} albums skipped due to not being able to open the yaml. Redownload the yaml file.")
    error_status = error_exists(origin_old)
    print(f"--{error_status}: There were {origin_old} origin files that do not have the needed metadata and need to be updated.")
    error_status = error_exists(bad_missing)
    print(f"--{error_status}: There were {bad_missing} folders missing an origin files that should have had them.")
    error_status = error_exists(good_missing)
    print(f"--Info: Some folders didn't have origin files and probably shouldn't have origin files. {good_missing} of these folders were identified.")

    if error_message >= 1:
        print("Check the logs to see which folders had errors and what they were.")
    else:
        print("There were no errors.")


# A function to check if the origin file is there and to determine whether it is supposed to be there.
def check_file(directory):
    global good_missing
    global bad_missing
    global origin_location

    # check to see if there is an origin file
    file_exists = os.path.exists("origin.yaml")
    # if origin file exists, load it, copy, and rename
    if file_exists == True:
        return True
    else:
        # split the directory to make sure that it distinguishes between foldrs that should and shouldn't have origin files
        current_path_segments = directory.split(os.sep)
        current_segments = len(current_path_segments)
        # create different log files depending on whether the origin file is missing somewhere it shouldn't be
        if origin_location != current_segments:
            # log the missing origin file folders that are likely supposed to be missing
            print("--An origin file is missing from a folder that should not have one.")
            print("--Logged missing origin file.")
            print("--This cannot be moved.")
            log_name = "good-missing-origin"
            log_message = "origin file is missing from a folder that should not have one.\nSince it shouldn't be there it is probably fine but you can double check"
            log_outcomes(directory, log_name, log_message)
            good_missing += 1  # variable will increment every loop iteration
            return False
        else:
            # log the missing origin file folders that are not likely supposed to be missing
            print("--An origin file is missing from a folder that should have one.")
            print("--Logged missing origin file.")
            print("--This should not be moved.")
            log_name = "bad-missing-origin"
            log_message = "origin file is missing from a folder that should have one"
            log_outcomes(directory, log_name, log_message)
            bad_missing += 1  # variable will increment every loop iteration
            return False


#  A function that gets the directory and then opens the origin file and extracts the needed variables
def get_creators(directory):
    global count
    global parse_error
    global origin_old

    print("\n")
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    print(f"Sorting {album_name}")

    # check to see if there is an origin file
    file_exists = check_file(directory)

    if file_exists == True:
        origin_path = os.path.join(directory, "origin.yaml")
        # open the yaml
        try:
            with open(origin_path, encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except:
            print("--There was an issue parsing the yaml file and the cover could not be downloaded.")
            print("--Logged missing cover due to parse error. Redownload origin file.")
            print("--This cannot be moved.")
            log_name = "parse-error"
            log_message = "had an error parsing the yaml and the cover art could not be downloaded. Redownload the origin file"
            log_outcomes(directory, log_name, log_message)
            parse_error += 1  # variable will increment every loop iteration
            return
        # check to see if the origin file has the corect metadata
        if "Cover" in data.keys():
            print("--You are using the correct version of gazelle-origin.")

            # turn the data into variables
            creators = {
                "start_path": directory,
                "album_directory": data["Directory"],
                "artist_name": data["Artist"],
                "dj_name": data["DJs"],
                "composer_name": data["Composers"],
                "conductor_name": data["Conductors"],
            }
            f.close()
            return creators
        else:
            print("--You need to update your origin files with more metadata.")
            print("--Switch to the gazelle-origin fork here: https://github.com/spinfast319/gazelle-origin")
            print("--Then run: https://github.com/spinfast319/Update-Gazelle-Origin-Files")
            print("--Then try this script again.")
            print("--Logged out of date origin file.")
            print("--This cannot be moved.")
            log_name = "out-of-date-origin"
            log_message = "origin file out of date"
            log_outcomes(directory, log_name, log_message)
            origin_old += 1  # variable will increment every loop iteration


# A function to move albums to the correct folder
def move_albums(move_list):
    global count

    # Loop through the list of albums to move
    for i in move_list:

        # Break each entry into a source and target
        start_path = i[0]
        target = i[1]

        # Move them to the folders they belong in
        print("")
        print("Moving.")
        print(f"--Source: {start_path}")
        print(f"--Destination: {target}")
        shutil.move(start_path, target)
        print("Move completed.")
        count += 1  # variable will increment every loop iteration


# A function to sort albums based on their creators and request them to be moved
def sort_albums(creators):
    global classical_directory
    global va_directory
    global dj_directory
    global log_directory
    global move_list
    global album_depth

    # creates filters for dj albums, classical albums and various artists with different paths for each
    if creators != None:
        start_path = creators["start_path"]
        if start_path != None:

            # get album name or artist-album name and create target path
            path_parths = start_path.split(os.sep)
            if album_depth == 1:
                album_name = path_parths[-1]
            elif album_depth == 2:
                aritist_name = path_parths[-2]
                album_name = path_parths[-1]
                album_name = os.path.join(aritist_name, album_name)

            # Sort the albums
            if creators["dj_name"] != None:
                print("--This should be moved to the DJ folder.")
                target = os.path.join(dj_directory, album_name)
                # make the pair a tupple
                move_pair = (start_path, target)
                # adds the tupple to the list
                move_list.append(move_pair)
            elif creators["composer_name"] != None or creators["composer_name"] != None:
                print("--This should be moved to the Classical folder.")
                target = os.path.join(classical_directory, album_name)
                # make the pair a tupple
                move_pair = (start_path, target)
                # adds the tupple to the list
                move_list.append(move_pair)
            elif creators["artist_name"] == "Various Artists":
                print("--This should be moved to the Various Artists folder.")
                target = os.path.join(va_directory, album_name)
                # make the pair a tupple
                move_pair = (start_path, target)
                # adds the tupple to the list
                move_list.append(move_pair)
            else:
                print("--This should not be moved.")


# The main function that controls the flow of the script
def main():
    global total_count
    global move_list

    try:
        # intro text
        print("")
        print("Do or do not...")
        print("")
        print("Part 1: Sorting")

        # Get all the subdirectories of album_directory recursively and store them in a list:
        directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
        directories.remove(os.path.abspath(album_directory))  # If you don't want your main directory included

        #  Run a loop that goes into each directory identified in the list and runs the function that sorts the folders
        for i in directories:
            os.chdir(i)  # Change working Directory
            creators = get_creators(i)  # Run function to get origin data
            sort_albums(creators)  # Filter out various artist, dj and classical albums for additional checks
            total_count += 1  # variable will increment every loop iteration

        # Change directory so the album directory can be moved and move them
        os.chdir(log_directory)

        # Move the albums to the folders the need to be sorted into
        print("")
        print("Part 2: Moving")
        move_albums(move_list)

    finally:
        # Summary text
        print("")
        print("There is no try...")
        # run summary text function to provide error messages
        summary_text()
        print("")


if __name__ == "__main__":
    main()
