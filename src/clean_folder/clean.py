import sys
import shutil
import os
import py7zr
from string import ascii_letters, digits


CATEGORIES = {'archives': ('zip', 'gz', 'tar', '7z'),
            'audio': ('mp3', 'ogg', 'wav', 'amr', 'flac'),
            'documents': ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'odt'),
            'images': ('jpeg', 'png', 'jpg', 'svg', 'webp'),
            'video': ('avi', 'mp4', 'mov', 'mkv')
            }

TRANSLITERATION = {'ї': 'yi', 'ё': 'yo', 'є': 'ye', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh',
                'з': 'z', 'и': 'y', 'і': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 
                'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 
                'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'Ё': 'Yo','Є': 'Ye', 'Ї': 'Yi', 'А': 'A', 'Б': 'B', 
                'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'І': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 
                'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 
                'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
                }  


def create_categories():
    """
    Create category folders if they don't exist.

    This function iterates over the defined categories and checks if each category folder
    exists in the BASE_FOLDER. If a category folder doesn't exist, it creates the folder.

    Args:
        None

    Returns:
        None
    """

    for folder_name in CATEGORIES:
        if folder_name in os.listdir(BASE_FOLDER):
            continue
        folder_path = os.path.join(BASE_FOLDER, folder_name)
        
        os.makedirs(folder_path)
        

def normalize(file_name: str) -> str:
    """
    Normalize the file name by removing illegal characters and applying transliteration.

    This function takes a file name as input and normalizes it by  replacing characters
    that are not in the set of allowed characters (ascii letters, digits, and underscore). 
    It also applies transliteration to replace any non-ASCII characters with their 
    corresponding ASCII equivalents.

    Args:
        file_name (str): The file name to normalize.

    Returns:
        str: The normalized file name."""

    correct_characters = ascii_letters + digits + '_'       
    file_name, extension = os.path.splitext(file_name)
    file_name = ''.join([char if char in correct_characters else TRANSLITERATION[char] 
                         if char in TRANSLITERATION else '_'
                         for char in file_name])   

    return file_name + extension


def check_name_conflict(folder_path: str, name: str) -> str:   
    """
    Check if a file name conflicts with existing files in a folder and resolves the conflict.

    This function checks if the given name conflicts with any existing files in the specified
    folder. If there is a conflict, it appends a counter to the name to make it unique.

    Args:
        folder_path (str): The path to the folder.
        name (str): The file name to check for conflicts.

    Returns:
        str: The resolved file name without conflicts.
    """

    files = os.listdir(folder_path)
    
    if name not in files:
        return name
        
    filename, extension = os.path.splitext(name)
    counter = 1
    new_filename = f"{filename}_{counter}{extension}"
    
    while new_filename in files:
        counter += 1
        new_filename = f"{filename}_{counter}{extension}"
    
    return new_filename
    

def rename_file(destination_folder: str, full_file_path: str) -> str: 
    """
    Rename a file and resolve naming conflicts.

    This function renames the file at the given full file path by normalizing the file name.
    If the new file name conflicts with existing files in either the source folder or the
    destination folder, it resolves the conflicts.

    Args:
        destination_folder (str): The path to the destination folder.
        full_file_path (str): The full path to the file.

    Returns:
        str: The new full file path of the renamed file.
    """

    file_name = os.path.basename(full_file_path)
    file_path = os.path.dirname(full_file_path) 

    new_file_name = normalize(file_name)
    if new_file_name != file_name:
        new_file_name = check_name_conflict(file_path, new_file_name)
    new_file_name = check_name_conflict(destination_folder, new_file_name)

    new_full_file_path = os.path.join(file_path, new_file_name)
      
    os.rename(full_file_path, new_full_file_path)

    return new_full_file_path


def move_file(file_path: str, destination_folder: str):
    """
    Move a file to the specified destination folder.

    This function moves the file at the given file path to the specified destination folder.
    It calls the `rename_file` function to ensure the file is renamed and conflicts are resolved
    before moving it.

    Args:
        file_path (str): The path to the file to be moved.
        destination_folder (str): The path to the destination folder.

    Returns:
        None
    """

    new_full_file_path = rename_file(destination_folder, file_path)
    shutil.move(new_full_file_path, destination_folder)


def get_category_path(file_name: str) -> str or None:
    """
    Get the category path for a file based on its extension.

    This function determines the category path for a file based on its extension. It compares
    the extension with the extensions defined in the CATEGORIES dictionary. If a match is found,
    it returns the corresponding category path.

    Args:
        file_name (str): The name of the file.

    Returns:
        str: The path to the category folder if the file belongs to a category, None otherwise.

    """

    extension = os.path.splitext(file_name)[1].lower()[1:]
    if extension:
    
        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                category_path = os.path.join(BASE_FOLDER, category)

                return category_path

    return None


def move_files():
    """
    Move files to their respective category folders.

    This function traverses the files and folders within the BASE_FOLDER.
    Files that match the extensions specified in the CATEGORIES dictionary are moved to their
    corresponding category folders using the move_file function.
    Files with unknown extensions are renamed using the rename_file function.

    Args:
        None

    Returns:
        None
    """ 
    
    for root, dirs, files in os.walk(BASE_FOLDER):
        if os.path.basename(root) in CATEGORIES:
            continue
        for file in files:
            category_path = get_category_path(file)
            if category_path:            
                move_file(os.path.join(root, file), category_path)
            else:
                rename_file(root, os.path.join(root, file))
            

def unpack_archives():
    """
    Unpack archive files within the 'archives' folder.

    This function extracts files from archive files located within the 'archives' folder
    of the BASE_FOLDER. It supports multiple archive formats such as zip, gz, tar, and 7z.
    Extracted files are placed in the 'archives' folder and the original archive files are deleted.

    Args:
        None

    Returns:
        None
    """ 
    
    folder_path = os.path.join(BASE_FOLDER, 'archives')
    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)

        if os.path.splitext(file)[1][1:] in CATEGORIES['archives']:

            if os.path.splitext(file)[1][1:] == '7z':
                with py7zr.SevenZipFile(file_path, mode='r') as z:
                    z.extractall(path=folder_path)
            else:
                shutil.unpack_archive(file_path, folder_path)

            os.remove(file_path)


def delete_empty_folders():
    """    
    Delete empty folders within the BASE_FOLDER.

    This function traverses the files and folders within the BASE_FOLDER in reverse order.
    Empty folders (excluding category folders) are deleted recursively.

    Args:
        None

    Returns:
        None    
    """

    for root, dirs, files in os.walk(BASE_FOLDER, topdown=False):        

        for directory in dirs:
            path = os.path.join(root, directory)
            
            if os.path.basename(path) in CATEGORIES:
                        continue

            if not os.listdir(path): 
                os.rmdir(path)


def rename_all_folders():
    """Rename all non-category folders.

    This function renames all non-category folders within the base folder by normalizing
    their names and resolving any conflicts with existing folders.

    Args:
        None

    Returns:
        None
    """ 

    for root, dirs, files in os.walk(BASE_FOLDER):
        for directory in dirs:

            if directory in CATEGORIES:
                continue

            new_folder_name = normalize(directory)

            if new_folder_name != directory:
               new_folder_name = check_name_conflict(root, new_folder_name)

            full_new_folder_name = os.path.join(root, new_folder_name) 
            full_old_folder_name = os.path.join(root, directory)          
            os.rename(full_old_folder_name, full_new_folder_name)


def disassemble_junk():
    """
    Perform the disassembly process.

    This function is the main entry point for the disassembly process.
    It calls various functions to create categories, move files, unpack archives,
    delete empty folders, and rename non-category folders.

    Args:
        None

    Returns:
        None
    """
    
    create_categories()
    move_files()
    unpack_archives()
    delete_empty_folders()
    rename_all_folders()


if __name__ == '__main__':
    
    if len(sys.argv) < 2:        
        BASE_FOLDER = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        BASE_FOLDER = sys.argv[1]
    
    disassemble_junk()    

    print("Sorting folder", BASE_FOLDER, "completed.")