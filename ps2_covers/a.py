import os
import json

# 1. Define that ZIP archive files are expected in the current working directory.
#    A single dot '.' represents the current directory.
#    So, the script will look for ZIP files in the same directory it is run from.
DIRECTORY_TO_SCAN = '.'

# 2. Define the name for the output JSON file.
#    This file will be created in the current working directory.
OUTPUT_JSON_FILE = 'game_archives.json'

# This list will store the information for each game archive found.
game_archives_list = []

# Get the current working directory (this will be your 'pwd' in Termux when you run the script).
current_working_directory = os.getcwd()

# The path to scan will be the current working directory.
# os.path.normpath cleans up the path (e.g. handles './' appropriately).
path_to_scan_zips = os.path.normpath(os.path.join(current_working_directory, DIRECTORY_TO_SCAN))

# Although '.' (current directory) should always be a valid directory,
# this check is kept for robustness.
if not os.path.isdir(path_to_scan_zips):
    # This situation is highly unlikely if DIRECTORY_TO_SCAN is '.'
    print(f"Error: The current working directory '{path_to_scan_zips}' is not accessible or is not a directory.")
    print("This is unexpected. Please check your current location and permissions.")
else:
    # Iterate over each item in the current working directory.
    for item_name in os.listdir(path_to_scan_zips):
        # Construct the full path to the item to check if it's a file.
        path_to_item = os.path.join(path_to_scan_zips, item_name)

        # Check if the current item is a file and ends with '.zip' (case-insensitive).
        if os.path.isfile(path_to_item) and item_name.lower().endswith('.zip'):
            # Extract the game ID by removing the '.zip' extension from the filename.
            # This assumes that the filename format is 'YourGameID.zip'.
            game_id = item_name[:-4]  # Removes the last 4 characters ('.zip')

            # Create a dictionary (object) for the current game archive.
            archive_entry = {
                "id": game_id,
                "archiveFile": item_name  # Storing only the filename, as it's in the same directory.
            }
            game_archives_list.append(archive_entry)

    # After checking all files, see if any archives were found.
    if game_archives_list:
        # (Optional) Sort the list alphabetically by the 'id' (Game ID).
        # This makes the output JSON file more organized.
        game_archives_list.sort(key=lambda entry: entry['id'])

        # Define the full path for the output JSON file (it will be in the current working directory).
        full_output_json_path = os.path.join(current_working_directory, OUTPUT_JSON_FILE)

        # Write the collected data to the JSON file.
        with open(full_output_json_path, 'w', encoding='utf-8') as f:
            json.dump(game_archives_list, f, ensure_ascii=False, indent=4)

        print(f"Successfully created '{OUTPUT_JSON_FILE}' in your current directory: {current_working_directory}")
        print(f"It contains {len(game_archives_list)} game archive entries.")
    else:
        # This message is shown if no .zip files were found in the current directory.
        print(f"No .zip files were found in the current directory: {current_working_directory}.")
        print(f"The file '{OUTPUT_JSON_FILE}' was not created or may be empty if it previously existed.")

