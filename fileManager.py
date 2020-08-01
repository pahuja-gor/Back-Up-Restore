# Organize the imports
import filecmp
import os
import shutil
import tarfile

class FileManager():

    src_path = input("Source Directory: ")
    dir_path = input("Destination Directory: ")

    def __init__(self, src_dir=src_path, dest_dir=dir_path):
        '''
        Creates a new FileManager object with two parameters:
            = The 'src' folder's filepath
            = The filepath for the back up folder (i.e. destination folder)

        :param src_dir: represents the 'src' folder's filepath (str)
        :param dest_dir: represents the filepath of the folder where the 'src' folder will be backed up to (str)
        '''
        self.src_dir = src_dir
        self.dest_dir = dest_dir
    
    def retrieve_src_dir(self):
        '''
        Returns the 'src' folder's filepath

        :return: the 'src' folder's filepath (str)
        '''
        return self.src_dir

    def retrieve_back_up_dir(self):
        '''
        Returns the back up/destination folder's filepath

        :return: the back up/destination folder's filepath (str)
        '''
        return self.dest_dir

    def check_empty_dir(self, dir):
        '''
        Checks if the specified directory 'dir' exists, and if it's empty or not.
        The function returns:
            = 0: The directory 'dir' exists and is NOT empty
            = 1: The directory 'dir' exists and is empty
            = 2: The directory 'dir' does not exist/was not found at the filepath provided

        :return: a value indicating whether the directory exists and if it's empty or not empty (int)
        '''
        try:
            dir_size = len(os.listdir(dir))
            if dir_size != 0:
                print("The directory isn't empty")
                return 2
            elif dir_size == 0:
                print("The directory is empty")
                return 1
        except FileNotFoundError:
            print("The directory doesn't exist at the filepath provided")
            return 0

    def copy_directory (self, src_dir, dest_dir):
        '''
        Copies the contents of the 'src_dir' directory into the 'dest_dir' directory

        :return: None
        '''
        empty_dir_value = self.check_empty_dir(dest_dir)
        if empty_dir_value == 0:
            print("Creating 'dest' and copying the content from 'src' to 'dest'...")
            shutil.copytree(src_dir, dest_dir)
            print('Finished copying...')
        elif empty_dir_value == 1 or empty_dir_value == 2:
            print("Deleting original 'dest' folder...")
            shutil.rmtree(dest_dir)
            print("Finished deleting original 'dest' folder...")
            print("Creating 'dest' and copying the content from 'src' to 'dest'...")
            shutil.copytree(src_dir, dest_dir)
            print('Finished copying...')

    def back_up_src(self):
        '''
        Takes a back up of the 'src' folder and stores it in its respective back up destination.
        Stores the back up in a '.tar' archive.

        :return: None
        '''
        print("Initiating Back Up...")
        print("Backing up the 'src' folder...")
        self.copy_directory(self.src_dir, self.dest_dir)
        print("Finished Backing up the 'src' folder")
        print("Back Up Complete!")

        with tarfile.open('src_archive' + '.tar.gz', mode='w:gz') as archive:
            archive.add(self.dest_dir, arcname=os.path.basename(self.dest_dir))

    def validate_back_up(self, src_dir, dest_dir):
        """
        Source:
        https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi

        Validates the back up by comparing the 'src_dir' and 'dest_dir' directories recursively.
        Files in each directory are assumed to be equal if their filenames and contents are equal.
        
        :param src_dir: represents the original source folder's filepath (str)
        :param dest_dir: represents the filepath of the folder where the back up is stored (str)
        
        :return: Whether both folders contain the same files or not [i.e. the back up is identical to the original source] (bool).
        """

        dirs_cmp = filecmp.dircmp(src_dir, dest_dir)
        if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0:
            return False
        (_, mismatch, errors) =  filecmp.cmpfiles(src_dir, dest_dir, dirs_cmp.common_files, shallow=False)
        if len(mismatch) > 0 or len(errors) > 0:
            return False
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(src_dir, common_dir)
            new_dir2 = os.path.join(dest_dir, common_dir)
            if not self.validate_back_up(new_dir1, new_dir2):
                return False
        return True

    def restore_back_up(self):
        '''
        Restores 'src' folder with its respective back up folder.

        :return: None
        '''
        print("Initiating Restore...")
        print("Restoring the 'src' folder...")
        self.copy_directory(self.dest_dir, self.src_dir)
        print("Finished restoring the 'src' folder")
        print("Restore Complete!")

# fManager = FileManager()
# fManager.back_up_src()