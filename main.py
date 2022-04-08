import requests
import os.path
import shutil
from datetime import date
import time

start = time.time()

addon_dir = "C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons"
download_dir = "C:/Users/kbh78/Downloads"

# Gets zip file from main ElvUI github repo
elvui_source_url = "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"
elvui_files = requests.get(elvui_source_url)

# Test 1
# if(type(addon_dir)!=str or type(download_dir)!=str or type(elvui_source_url)!=str):
#     exit()

# Creates timestamp(s) on zip for organizational purposes (backups, versions, etc.)
today = date.today()
date_format = today.strftime("%Y-%m-%d")

# Writes zip file to local downloads folder
with open(f"{download_dir}/ElvUI-main {date_format}.zip", "wb") as file:
    file.write(elvui_files.content)

# Specifies parameters for unzipping file
file_name = f"{download_dir}/ElvUI-main {date_format}.zip"
archive_format = "zip"

# Unzips file
shutil.unpack_archive(file_name, download_dir, archive_format)

elvui_dir_list = ["/ElvUI", "/ElvUI_OptionsUI"]

# for i in range(len(elvui_dir_list)):
for i, value in enumerate(elvui_dir_list):
    
# Checks if backup folders exist from previous updates
    if(os.path.exists(f"{addon_dir}{elvui_dir_list[i]}_OLD")):
        shutil.rmtree(f"{addon_dir}{elvui_dir_list[i]}_OLD")
        
# Checks if active folders exist, and renames them as a form of backup to make way for updated versions
    if(os.path.exists(f"{addon_dir}{elvui_dir_list[i]}")):
        os.rename(f"{addon_dir}{elvui_dir_list[i]}", f"{addon_dir}{elvui_dir_list[i]}_OLD")

# Moves files from unzipped ElvUI folder to game/addon directory
    shutil.move(f"{download_dir}/ElvUI-main{elvui_dir_list[i]}", f"{addon_dir}")

# Removes empty unzipped ElvUI folder
shutil.rmtree(f"{download_dir}/ElvUI-main")

# End of Program
end = time.time()
print(f"Completed in {round((end-start), 2)} seconds.")

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
