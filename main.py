from fileManager import *

fileManager = FileManager()

cmd = input('Enter Command: ')

while (cmd.lower() != 'exit'):
    if (cmd.lower() == 'backup'):
        fileManager.back_up_src()
        cmd = input('Enter Command: ')
    elif (cmd.lower() == 'restore'):
        fileManager.restore_back_up()
        cmd = input('Enter Command: ')
    else:
        cmd = input('Enter Command: ')
print('Exited Successfully :)')