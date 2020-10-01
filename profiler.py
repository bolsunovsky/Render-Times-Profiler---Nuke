
import sys
import os.path
import nuke
from timeit import default_timer as timer
import json
import math

# Renders all nuke scripts in a directory with Write node "Write1" present. Outputs render times to a JSON file in a { 'name': [time] } format. Prints average time of a render script set (number of renders can be changed in renderCount for more accurate render time per script)

# Invoke script with arguments:
# Nuke -t(i) (file: script path) (directory: .nk scrips path) (file: output JSON path)



# .nk directory read path.
readPath = (sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1] + '/')

# JSON file path.
savePath = sys.argv[2]

# Amount of times the script is rerendered.
renderCount = 3

# Amount of frames to render per render count.
framesToRender = 24

nkScripts = []
renderTimeResults = []
jsonResults = {}

_currentScript = ""

def updateJSON(data):
    f = open(savePath, "w")
    json.dump(data, f)

# Set current .nk script.
def setCurrentScript(newScript):
    global _currentScript
    changed = _currentScript != (newScript)
    if changed:
        _currentScript = newScript


def getCurrentScript():
    return _currentScript
# TODO: add more checks.
for script in os.listdir(readPath):
    if script.endswith(".nk"):
        nkScripts.append(script)
        if len(nkScripts) > 0:
            setCurrentScript(nkScripts[0])

    
nuke.scriptOpen(readPath + getCurrentScript())



# Recursively render the scripts repeating based on number of interation.
def executeWrite(renderCount):
    for i in range(renderCount):
        nuke.execute('Write1', 1, framesToRender, 1)
        
        if i == (renderCount - 1):
            jsonResults[getCurrentScript()] = renderTimeResults
            
            averageRenderTime = math.floor(sum(renderTimeResults) / len(renderTimeResults) * 100)/100.0
            # report average write time of the same script renders.
            print('Finished rendering ' + getCurrentScript() + ' with an average render time of ' + str(averageRenderTime) + ' seconds')
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

# Times and updates render times.
def endRender():
    renderTimeResults.append(timer() - startTime)
    print('Finished rendering ' + getCurrentScript())


nuke.addBeforeRender(startRender)
nuke.addAfterRender(endRender)


executeWrite(renderCount)
    

