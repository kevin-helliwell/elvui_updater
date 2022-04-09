# elvui_updater

Updates ElvUI and ElvUI_OptionsUI folders using latest files from Tukui repo.

What this program requires to function:

(1) An internet connection (to fetch latest version)

(2) An addon directory (destination)

(3) A downloads or other directory (to store zip file before program can unzip and move files to addon directory)

What this program does:

(1) Gets current version number of ElvUI from official github repository via API GET request

(2) Checks if zip file of current version exists already in downloads directory

(a) If yes, exits program

(3) Downloads latest version of ElvUI from official github repository as a zip file to downloads directory

(4) Adds timestamp to zip file

(5) Unzips file, returns folder with files in it

(6) Looks inside folder:

(a) Checks if matching files with \_OLD suffix exist already in addon directory:

If true, deletes files with \_OLD suffix

**NOTE: This basically checks if this program has been run already so that it doesn't block itself in the next step.**

(b) Checks if matching files exist already in addon directory:

If true, adds OLD suffix to file names in addon directory

(7) Moves files from folder to addon directory

(8) Deletes folder
