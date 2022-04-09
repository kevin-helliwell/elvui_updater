# Dependencies
import requests
import os.path
import shutil
from datetime import date
import time
import json

#------------------------------------------------------------------------------------------------------------------------

# Destination directory for new files to go
addon_dir = "C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons"

# Source directory for downloaded files 
download_dir = "C:/Users/kbh78/Downloads"

# Starts timer
start = time.time()

# Get version number
API_url = "https://api.github.com/repos/tukui-org/ElvUI/branches/main"
API_data = requests.get(API_url).text
parse_json_data = json.loads(API_data)
version_number = parse_json_data.get("commit").get("commit").get("message")

# Checks if current version already exists
download_dir_list = os.listdir(download_dir)
if(download_dir_list.count(f"ElvUI-main {version_number}.zip")>0):
    exit(f"Current version already exists in {download_dir}")

# Gets zip file from main ElvUI github repo
elvui_source_url = "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"
elvui_files = requests.get(elvui_source_url)

# Writes zip file to local downloads folder
# Appends version number for validation
elvui_main = f"{download_dir}/ElvUI-main"
with open(f"{elvui_main} {version_number}.zip", "wb") as file:
    file.write(elvui_files.content)

# Specifies parameters for unzipping file
file_name = f"{elvui_main} {version_number}.zip"
archive_format = "zip"

# Unzips file
shutil.unpack_archive(file_name, download_dir, archive_format)

# List of directory names to check for and move
elvui_dir_list = os.listdir(elvui_main)

# Generates directory paths and checks if they exist already
for i, _ in enumerate(elvui_dir_list):
    
    # Checks if any old version of elvui exists in game/addon directory
    # (Checks if this program has been run before)
    old_path = os.path.join(addon_dir, f"{elvui_dir_list[i]}_OLD")
    old_path_exists = os.path.exists(old_path)
    
    # Checks if current version of elvui exists in game/addon directory
    # (If no current version exists, then we don't have to make room for it in game/addon directory! :D)
    current_path = os.path.join(addon_dir, elvui_dir_list[i])
    current_path_exists = os.path.exists(current_path)

# Checks if backup folders exist from previous updates
    if(old_path_exists):
        shutil.rmtree(old_path)
        
# Checks if active folders exist, and renames them as a form of backup to make way for updated versions
    if(current_path_exists):
        os.rename(current_path, old_path)

# Moves files from unzipped ElvUI folder in downloads directory to game/addon directory
    new_path = os.path.join(elvui_main, elvui_dir_list[i])
    shutil.move(new_path, addon_dir)

# Removes empty unzipped ElvUI folder in downloads directory
shutil.rmtree(elvui_main)

# End of Program
end = time.time()
print(f"Completed in {round((end-start), 2)} seconds.")

#------------------------------------------------------------------------------------------------------------------------

# OLDER VERSIONS OF CODE FROM VARIOUS SECTIONS (DISREGARD)

# for i in range(len(elvui_dir_list)):
# old_path = f"{addon_dir}{elvui_dir_list[i]}_OLD"
# current_path = f"{addon_dir}{elvui_dir_list[i]}"
# new_path = f"{elvui_main}{elvui_dir_list[i]}"

# OLD SLOWER WAY
# if(os.path.exists(f"{addon_dir}/ElvUI_OLD")):
#     shutil.rmtree(f"{addon_dir}/ElvUI_OLD")
# if(os.path.exists(f"{addon_dir}/ElvUI_OptionsUI_OLD")):
#     shutil.rmtree(f"{addon_dir}/ElvUI_OptionsUI_OLD")

# OLD WAY
# if(os.path.exists(f"{addon_dir}/ElvUI")):
#     os.rename(f"{addon_dir}/ElvUI", f"{addon_dir}/ElvUI_OLD")
# if(os.path.exists(f"{addon_dir}/ElvUI_OptionsUI")):
#     os.rename(f"{addon_dir}/ElvUI_OptionsUI", f"{addon_dir}/ElvUI_OptionsUI_OLD")

# OLD WAY
# shutil.move(f"{download_dir}/ElvUI-main/ElvUI", f"{addon_dir}")
# shutil.move(f"{download_dir}/ElvUI-main/ElvUI_OptionsUI", f"{addon_dir}")

# Test 1
# if(type(addon_dir)!=str or type(download_dir)!=str or type(elvui_source_url)!=str):
#     exit()

# # elvui_dir_list = ["ElvUI", "ElvUI_OptionsUI"]

# Initializes today's date for next code block
# today = date.today()
# date_format = today.strftime("%Y-%m-%d")