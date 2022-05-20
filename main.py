# Dependencies
import requests
import os.path
import shutil
import time
import json


class AddonManager:

    # Constructor logic
    def __init__(self, addon_dir, download_dir, api_url, source_url):
        self.addon_dir = addon_dir
        self.download_dir = download_dir
        self.api_url = api_url
        self.source_url = source_url

    # Methods

    # Gets version number from main ElvUI GitHub repo
    def get_version_number(self):
        api_data = requests.get(self.api_url).text
        parse_json_data = json.loads(api_data)
        version_number = parse_json_data.get("commit").get("commit").get("message")
        return version_number

    # Gets zip file name from main ElvUI GitHub repo by splitting and joining parts of the repo URL
    def get_zip_file_name(self):
        url_split_list = self.api_url.rsplit("/")
        zip_file_name = f"{url_split_list[-3]}-{url_split_list[-1]}"
        return zip_file_name

    # Checks if current version already exists in downloads directory
    def check_local_version(self):
        download_dir_list = os.listdir(self.download_dir)
        zip_file_name = self.get_zip_file_name()
        version_number = self.get_version_number()
        if download_dir_list.count(f"{zip_file_name} {version_number}.zip") > 0:
            end_timer = time.time()
            exit(
                f"Current version already exists in {self.download_dir}\n"f"Completed in {round((end_timer - start_timer), 2)} seconds")
        return self

    # Gets source zip file data from an API request before being written to a file in another function
    def get_source_zip_data(self):
        zip_file_data = requests.get(self.source_url).content
        return zip_file_data

    # Gets file path in download directory for zip file data to be written to in another function
    def get_zip_file_path(self):
        zip_file_path = f"{self.download_dir}/{self.get_zip_file_name()}"
        return zip_file_path

    # Writes zip file to local "downloads" directory
    # Appends version number for validation
    def manage_zip(self):
        zip_file_path = self.get_zip_file_path()
        version_number = self.get_version_number()
        file_name = f"{zip_file_path} {version_number}.zip"
        source_zip_data = self.get_source_zip_data()

        with open(file_name, "wb") as file:
            file.write(source_zip_data)

        # Specifies parameter for unzipping file
        archive_format = "zip"

        # Unzips file
        shutil.unpack_archive(file_name, self.download_dir, archive_format)

        return self

    # Manages file paths in downloads and game/addons directories based on API data
    def manage_paths(self):
        # List of directory names to check for and move
        zip_file_path = self.get_zip_file_path()
        zip_dir_list = os.listdir(zip_file_path)

        # Generates directory paths and checks if they exist already
        for i, _ in enumerate(zip_dir_list):

            # Checks if any old version of ElvUI exists in game/addon directory
            # Implicitly checks if this program has been run before
            old_path = os.path.join(self.addon_dir, f"{zip_dir_list[i]}_OLD")
            old_path_exists = os.path.exists(old_path)

            # Checks if any current version of ElvUI exists in game/addon directory
            # If no current version exists, then we don't have to make room for it in game/addon directory! :D
            current_path = os.path.join(self.addon_dir, zip_dir_list[i])
            current_path_exists = os.path.exists(current_path)

            # Checks if backup folders exist from previous updates
            if old_path_exists:
                shutil.rmtree(old_path)

            # Renames matching files if they exist already in your game/addon directory
            if current_path_exists:
                os.rename(current_path, old_path)

            # Moves the files extracted from unzipped ElvUI folder in downloads directory to game/addon directory
            new_path = os.path.join(zip_file_path, zip_dir_list[i])
            shutil.move(new_path, self.addon_dir)

        # Removes empty unzipped ElvUI folder in downloads directory
        shutil.rmtree(zip_file_path)

        return self


# Program
def main():
    # Sets necessary parameters for program to run
    config_values = ("C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons", "C:/Users/kbh78/Downloads",
                     "https://api.github.com/repos/tukui-org/ElvUI/branches/main",
                     "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip")

    # addon_dir: Destination directory for new files to go
    # download_dir: Source directory for downloaded files
    # api_url: Where ElvUI API data is located
    # source_url: Where ElvUI zip file is located
    addon_dir, download_dir, api_url, source_url = config_values

    # Creates ElvUI manager with class constructor
    ui_manager = AddonManager(addon_dir, download_dir, api_url, source_url)

    # Checks if current version already exists in downloads directory
    # Writes zip file to local "downloads" folder, appends version number for validation, and unzips file

    # Deletes folders with "_old" suffix and renames current folders with "_old" suffix if they exist
    # Moves files from unzipped folder to game/addons directory and deletes unzipped folder
    ui_manager.check_local_version().manage_zip().manage_paths()


if __name__ == "__main__":
    # Starts timer
    start_timer = time.time()

    # Runs program
    main()

    # End of Program
    end_timer = time.time()
    print(f"Completed in {round((end_timer - start_timer), 2)} seconds")

# OLDER VERSIONS OF CODE FROM VARIOUS SECTIONS (DISREGARD)

# for i in range(len(zip_dir_list)):
# old_path = f"{addon_dir}{zip_dir_list[i]}_OLD"
# current_path = f"{addon_dir}{zip_dir_list[i]}"
# new_path = f"{zip_file_path}{zip_dir_list[i]}"

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
# if(type(addon_dir)!=str or type(download_dir)!=str or type(source_url)!=str):
#     exit()

# # zip_dir_list = ["ElvUI", "ElvUI_OptionsUI"]

# Initializes today's date for next code block
# today = date.today()
# date_format = today.strftime("%Y-%m-%d")

# # List of directory names to check for and move
# zip_dir_list = os.listdir(zip_file_path)

# # Generates directory paths and checks if they exist already
# for i, _ in enumerate(zip_dir_list):

#     # Checks if any old version of elvui exists in game/addon directory
#     # (Checks if this program has been run before)
#     old_path = os.path.join(addon_dir, f"{zip_dir_list[i]}_OLD")
#     old_path_exists = os.path.exists(old_path)

#     # Checks if current version of elvui exists in game/addon directory
#     # (If no current version exists, then we don't have to make room for it in game/addon directory! :D)
#     current_path = os.path.join(addon_dir, zip_dir_list[i])
#     current_path_exists = os.path.exists(current_path)

# # Checks if backup folders exist from previous updates
#     if(old_path_exists):
#         shutil.rmtree(old_path)

# # Checks if active folders exist, and renames them as a form of backup to make way for updated versions
#     if(current_path_exists):
#         os.rename(current_path, old_path)

# # Moves files from unzipped ElvUI folder in downloads directory to game/addon directory
#     new_path = os.path.join(zip_file_path, zip_dir_list[i])
#     shutil.move(new_path, addon_dir)

# Checks if current version already exists
# download_dir_list = os.listdir(download_dir)
# if(download_dir_list.count(f"ElvUI-main {get_version_number()}.zip")>0):
#     end = time.time()
#     exit(f"Current version already exists in {download_dir} \n "f"Completed in {round((end-start), 2)} seconds")

# # Gets zip file from main ElvUI github repo
# source_url = "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"
# elvui_files = requests.get(source_url)

# with open(f"{zip_file_path} {get_version_number()}.zip", "wb") as file:
#     file.write(get_source_zip_data().content)

# # Specifies parameters for unzipping file
# file_name = f"{zip_file_path} {get_version_number()}.zip"
# archive_format = "zip"

# # Unzips file
# shutil.unpack_archive(file_name, download_dir, archive_format)

# Checks for old and current versions
# Moves files accordingly and deletes empty unzipped folder

# Gets zip file from main ElvUI github repo
# def get_source_zip_data():
#     source_url = "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"
#     elvui_files = requests.get(source_url)
#     return elvui_files

# zip_file_path = f"{download_dir}/{zip_file_name}"

# API_url = "https://api.github.com/repos/tukui-org/ElvUI/branches/main"

# addon_dir = "C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons"
# download_dir = "C:/Users/kbh78/Downloads"
# api_url = "https://api.github.com/repos/tukui-org/ElvUI/branches/main"
# source_url = "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"

# url_split_list = api_url.rsplit("/")
# zip_file_name = f"{url_split_list[-3]}-{url_split_list[-1]}"

# config_dict = {"addon_dir":"C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons", "download_dir":"C:/Users/kbh78/Downloads", "api_url": "https://api.github.com/repos/tukui-org/ElvUI/branches/main", "source_url": "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"}

# Destination directory for new files to go
# addon_dir = config_dict.get("addon_dir")

# Source directory for downloaded files 
# download_dir = config_dict.get("download_dir")

# Where elvui API data is located
# api_url = config_dict.get("api_url")

# Where elvui zip file is located
# source_url = config_dict.get("source_url")

# config_dict = dict(zip(config_keys, config_values))
# addon_dir, download_dir, api_url, source_url = config_dict.values()

# elvui_manager.manage_zip()
# elvui_manager.manage_paths()

# Starts timer
# start = time.time()

# End of Program
# end = time.time()
# print(f"Completed in {round((end-start), 2)} seconds")
