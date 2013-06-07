
import os
import time


class Observer(object):

    def __init__(self, observ_dir, mod_period, exclude_extensions):
        self.observDirectory = observ_dir
        self.modificationPeriod = mod_period
        self.excludeExtensions = exclude_extensions
        self.modifiedList = []


    def run(self):

        self.modifiedList = []
        for d, dirs, files in os.walk(self.observDirectory):
            for f in files:
                path = os.path.join(d,f)
                
                # skipping files from exclude list
                fileExtension = os.path.splitext(path)[1].replace('.', '')
                if fileExtension in self.excludeExtensions:
                    continue

                modTime = os.path.getmtime(path)
                createTime = os.path.getctime(path)
                noModDuration = time.time() - modTime
                noCreateDuration = time.time() - createTime
                if noCreateDuration <= self.modificationPeriod:
                    self.modifiedList.append( {'filePath' : path, 'modTimestamp': modTime,'modTime' : noCreateDuration, 'changeType' : 'A'} )
                elif noModDuration <= self.modificationPeriod:
                    self.modifiedList.append( {'filePath' : path, 'modTimestamp': modTime, 'modTime' : noModDuration, 'changeType' : 'M'} )

        return self.modifiedList