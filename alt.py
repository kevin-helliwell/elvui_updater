# Dependencies
import requests
import os.path
import shutil
import time
from datetime import date

class AddonManager:
    
    # Constructor logic
    def __init__(self, addon_dir, download_dir, source_url):
        self.addon_dir = addon_dir
        self.download_dir = download_dir
        self.source_url = source_url
        
    # Methods
    
    # Gets zip file name from github repo by splitting and joining parts of the zip file source URL
    def get_zip_file_name(self):
        if self.source_url.count("ElvUI")>0:
            url_split_list = self.source_url.rsplit("/")
            name = url_split_list[-5]
            branch = url_split_list[-1].rsplit(".")[-2]
            zip_file_name = f"{name}-{branch}"
            return zip_file_name
    
    # Checks if current version already exists in downloads directory
    def check_backup(self):
        today = date.today()
        date_format = today.strftime("%Y-%m-%d")
        download_dir_list = os.listdir(self.download_dir)
        zip_file_name = self.get_zip_file_name()
        if(download_dir_list.count(f"{zip_file_name} {date_format}.zip")>0):
            end = time.time()
            exit(f"Current version already exists in {self.download_dir}\n"f"Completed in {round((end-start), 3)} seconds")
        return self
    
    # Gets source zip file data from an HTTP GET request before being written to a file in another function
    def get_source_zip_data(self):
        zip_file_data = requests.get(self.source_url).content
        return zip_file_data
    
    # Gets file path in download directory for zip file data to be written to in another function
    def get_zip_file_path(self):
        zip_file_path = f"{self.download_dir}/{self.get_zip_file_name()}"
        return zip_file_path
        
    # Writes zip file to local downloads directory
    # Appends version number for validation
    def manage_zip(self):
        
        zip_file_path = self.get_zip_file_path()
        file_name = f"{zip_file_path}.zip"
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
            
            # Checks if any old version of elvui exists in game/addon directory
            # Implicitly checks if this program has been run before
            old_path = os.path.join(self.addon_dir, f"{zip_dir_list[i]}_OLD")
            old_path_exists = os.path.exists(old_path)
            
            # Checks if any current version of elvui exists in game/addon directory
            # If no current version exists, then we don't have to make room for it in game/addon directory! :D
            current_path = os.path.join(self.addon_dir, zip_dir_list[i])
            current_path_exists = os.path.exists(current_path)
            
            # Checks if backup folders exist from previous updates
            if(old_path_exists):
                shutil.rmtree(old_path)
            
            # Renames matching files if they exist already in your game/addon directory
            if(current_path_exists):
                os.rename(current_path, old_path)
            
            # Moves files from unzipped ElvUI folder in downloads directory to game/addon directory
            new_path = os.path.join(zip_file_path, zip_dir_list[i])
            shutil.move(new_path, self.addon_dir)
        
        # Deletes unzipped elvui-main folder and elvui-main.zip in downloads directory
        today = date.today()
        date_format = today.strftime("%Y-%m-%d")
        
        shutil.rmtree(zip_file_path)
        os.rename(f"{zip_file_path}.zip", f"{zip_file_path} {date_format}.zip")
        
        return self
        
# Program

def main():
    
    # Sets necessary parameters for program to run
    local_directories = ("C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons", "C:/Users/kbh78/Downloads")
    source_urls_list = ["https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"]
    
    for i, _ in enumerate(source_urls_list):
        # addon_dir: Destination directory for new files to go
        # download_dir: Source directory for downloaded files
        # source_url: Where zip files are located
        (addon_dir, download_dir), source_url = local_directories, source_urls_list[i]
        
        # Creates elvui manager with class constructor
        elvui_manager = AddonManager(addon_dir, download_dir, source_url)

        # Checks if zip file exists already with today's date
        # Writes zip file to local downloads folder
        # Deletes folders with "_old" suffix and renames current folders with "_old" suffix if they exist
        # Moves files from unzipped folder to game/addons directory. deletes unzipped folder and renames zip file with today's date
        elvui_manager.check_backup().manage_zip().manage_paths()

if __name__ == "__main__":
        
    # Starts timer
    start = time.time()
            
    # Runs program
    main()
            
    # End of Program
    end = time.time()
    print(f"Completed in {round((end-start), 3)} seconds")