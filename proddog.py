
import os
import time
import math

import proddog.changeset
import proddog.observer


observDirectory = '/var/local/www/hostname'
modifiedPeriod = 60*60*48
checkPeriod = 10*60
excludeExtensions = ['png', 'log']

observer = prodcontrol.observer.Observer(observDirectory, modifiedPeriod, excludeExtensions)
changeset = prodcontrol.changeset.Changeset('.changeset')

while True:
    os.system('cls' if os.name=='nt' else 'clear') 
    print "-"*50
    print "[{0}]: started check\n".format(time.asctime( time.localtime(time.time()) ))
    modifiedFiles = observer.run()
    

    changesetList = []
    for modifiedFile in modifiedFiles:

        # updating changeset file
        if changeset.hasChange(modifiedFile['filePath'], modifiedFile['modTimestamp']):
            continue        
        changeset.addChange(modifiedFile['filePath'], modifiedFile['modTimestamp'])
        changesetList.append(modifiedFile)

    if len(changesetList) <= 0:
        print "\t No new changes found"

    
    # output changeset
    for modifiedFile in changesetList:

        # converting modTime seconds to human-readable text
        modificationTime = ''
        modHours = 0
        modMinutes = 0
        if int(modifiedFile['modTime']) > 3600:
            modHours = int(modifiedFile['modTime'] / 3600)
        if int(modifiedFile['modTime']) - modHours*3600 > 60:
            modMinutes = int((modifiedFile['modTime'] - modHours*3600) / 60)
        
        if modHours > 0:
            modificationTime += str(modHours) + "h "
        if modMinutes > 0:
            modificationTime += str(modMinutes) + "m "
        if int(modifiedFile['modTime']) - modHours*3600 - modMinutes*60 > 0:
            modificationTime += str(int(modifiedFile['modTime']) - modHours*3600 - modMinutes*60) + "s"
        # / converted

        print "\t[{0}]: {1} (-{2})".format(modifiedFile['changeType'], modifiedFile['filePath'], modificationTime)

    print "\n[{0}]: done".format(time.asctime( time.localtime(time.time()) ))
    time.sleep(checkPeriod)
