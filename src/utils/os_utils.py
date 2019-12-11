import os

def makedirs_if_doesnt_exist(path):
    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(path)
        print("Directory ", path, " Created ")
    except FileExistsError:
        pass
        #print("Directory ", path, " already exists")

