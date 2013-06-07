
import os

class Changeset(object):

    def __init__(self, changeset_path):
        self.changesetPath = changeset_path


    def hasChange(self, filename, change_time):

        # always returns False if changeset file not exists
        if not os.path.exists(self.changesetPath):
            return False

        changesetFile = open(self.changesetPath)
        for changeInfo in changesetFile.readlines():
            if (filename in changeInfo) and (str(change_time) in changeInfo):
                changesetFile.close()
                return True
        changesetFile.close()

        return False


    def addChange(self, filename, change_time):
        changesetFile = open(self.changesetPath, 'a')
        changesetFile.write(filename + ';' + str(change_time) + "\n")
        changesetFile.close()
