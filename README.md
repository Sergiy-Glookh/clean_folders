Clean Folder

Clean Folder is a Python script that helps you organize and sort files in a specified folder based on their file extensions. It provides a convenient way to declutter your folders and keep your files neatly categorized.


Features

Recursively sorts files in the target folder and its subfolders.
Supports various file categories, including archives, audio files, documents, images, and videos.
Normalizes file names by transliterating Cyrillic characters to Latin characters and replacing non-alphanumeric characters with underscores.
Handles name conflicts by appending a counter to the file name.
Automatically unpacks archive files (ZIP, GZ, TAR, 7Z) and moves their contents to the appropriate folder.
Deletes empty folders after the sorting process.


Installation

To install Clean Folder, follow these steps:
1. Clone or download the Clean Folder repository from GitHub https://github.com/Sergiy-Glookh/clean-folder.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the following command to install the package:
   pip install -e .
Note: You may need administrator privileges to install the package system-wide.


Usage

Once Clean Folder is installed, you can use it as a command-line tool.
To sort files in a folder, navigate to the folder you want to sort and run the following command:
   clean-folder [folder_path]
Replace [folder_path] with the path to the folder you want to clean. If you don't provide a folder path, the script will clean the folder where the clean-folder script is located.
Clean Folder will organize the files in the folder and its subfolders according to their file extensions and display a message once the sorting is complete.
Please note that Clean Folder ignores the pre-defined folders (archives, audio, documents, images, video) to prevent moving files that have already been sorted.

Customization

You can customize the script by modifying the file categories and their corresponding file extensions. Open the sort.py file and update the CATEGORIES dictionary as desired.

CATEGORIES = {
    'archives': ('zip', 'gz', 'tar', '7z'),
    'audio': ('mp3', 'ogg', 'wav', 'amr', 'flac'),
    'documents': ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'odt'),
    'images': ('jpeg', 'png', 'jpg', 'svg', 'webp'),
    'video': ('avi', 'mp4', 'mov', 'mkv')
}

Feel free to add or remove file extensions and adjust the category names to suit your preferences.


Requirements

Clean Folder requires Python 3 to be installed on your system.


License

This project is licensed under the MIT License. See the LICENSE file for more information.
