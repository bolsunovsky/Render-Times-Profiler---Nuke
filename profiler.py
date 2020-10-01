import sys
import os.path
import nuke
from timeit import default_timer as timer
import json

# renders all nuke scripts in a directory with Write node "Write1" present. Outputs render times to a JSON file in a { 'name': [time] } format.

# invoke script with arguments:
# nuke -t(i) (file: script path) (directory: .nk scrips path) (file: output JSON path)



#.nk directory read path
readPath = (sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1] + '/')

#JSON file path
savePath = sys.argv[2]

renderCount = 3

nkScripts = []
renderTimeResults = []
jsonResults = {}

_currentScript = ""

def updateJSON(data):
    f = open(savePath, "w")
    json.dump(data, f)
    f.close()

# set current .nk script
def setCurrentScript(newScript):
    global _currentScript
    changed = _currentScript != (newScript)
    if changed:
        _currentScript = newScript


def getCurrentScript():
    return _currentScript

for script in os.listdir(readPath):
    if script.endswith(".nk"):
        nkScripts.append(script)
        if len(nkScripts) > 0:
            setCurrentScript(nkScripts[0])

    
nuke.scriptOpen(readPath + getCurrentScript())



# recursively render the scripts repeating based on number of interation
def executeWrite(renderCount):
    for i in range(renderCount):
        nuke.execute('Write1', 1,30, 1)
        
        if i == (renderCount - 1):
            jsonResults[getCurrentScript()] = renderTimeResults
            updateJSON(jsonResults)

            global renderTimeResults
            renderTimeResults = []

            currentScriptIndex = nkScripts.index(getCurrentScript())
            if currentScriptIndex + 1 < len(nkScripts):
                
                setCurrentScript(nkScripts[currentScriptIndex + 1])
                executeWrite(renderCount)
                


startTime = timer()


def startRender():
    global startTime
    startTime = timer()
    print('Starting rendering ' + getCurrentScript())

# note time and update data
def endRender():
    renderTimeResults.append(timer() - startTime)
    print('Finished rendering ' + getCurrentScript())


#adding callbacks for time tracking
nuke.addBeforeRender(startRender)
nuke.addAfterRender(endRender)


executeWrite(renderCount)
    

