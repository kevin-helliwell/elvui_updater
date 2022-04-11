# elvui_updater

Updates ElvUI and ElvUI_OptionsUI folders using latest files from Tukui repo (https://github.com/tukui-org/ElvUI/tree/main).

What this requires:

- An internet connection (to fetch latest version)

- An addon directory (destination)

- A downloads or other directory (to store zip file before program can unzip and move files to addon directory)

How it works:

- Gets current version number of ElvUI from official github repository via API GET request

- Checks if zip file of current version exists already in downloads directory

- If yes, exits program

- Downloads latest version of ElvUI from official github repository as a zip file to downloads directory

- Adds timestamp to zip file

- Unzips file, returns folder with files in it

- Looks inside folder

- Checks if matching files with \_OLD suffix exist already in addon directory

- If true, deletes files with \_OLD suffix

**NOTE: This basically checks if this program has been run already so that it doesn't block itself in the next step.**

- Checks if matching files exist already in addon directory

- If true, adds OLD suffix to file names in addon directory

- Moves files from folder to addon directory

- Deletes folder
