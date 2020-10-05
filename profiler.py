
import sys
import os.path
import nuke
from timeit import default_timer as timer
import json
import math

# Renders all nuke scripts in a directory with Write node "Write1" present. Outputs render times to a JSON file in a { 'name': [time] } format. Prints average time of a render script set (number of renders can be changed in renderCount for more accurate render time per script)

# Invoke script with arguments:
# Nuke -t(i) (file: script path) (directory: .nk scrips path) (file: output JSON path)

# Platform Type
from sys import platform as __platform
if __platform == "linux" or __platform == "linux2":
    _platform = 'linux'
elif __platform == "darwin":
    _platform = 'osx'
elif __platform == "win32":
    _platform = 'win'


# Check if path is to a file
def checkFilePath(path):
    if os.path.isfile(path): return path
    else: raise TypeError("Third argument must be a file")

# Check if file is of JSON format
def checkJsonFormat(path):
    if path.endswith(".json"): return path
    else: raise TypeError("File must end with .json")

# Check if path is a directory
def checkDirectoryPath(path):
    if os.path.isdir(path): return path
    else: raise TypeError("Second argument must be a directory")
        
# Checks for .nk script presence in the given directory
def findNukeScripts(path):
    nukeScripts = filter(lambda script: script.endswith(".nk"), os.listdir(path))
    if len(nukeScripts) > 0: return nukeScripts
    else: raise LookupError("No Nuke scripts found in the directory")
    
# Check if running on a compatible os. TODO: test other platforms.
def _checkPlatform(platform):
    if platform == 'osx': pass
    else: raise ImportWarning(platform + " has not been tested yet. Unstable.")

_checkPlatform(_platform)

# .nk directory read path.
readPath = checkDirectoryPath(sys.argv[1])


# JSON file path.
savePath = checkJsonFormat((checkFilePath(sys.argv[2])))

# Amount of times the script is rerendered.
renderCount = 3

# Amount of frames to render per render count.
framesToRender = 24

# Declarations.
nukeScripts = findNukeScripts(path = readPath)
print(nukeScripts)
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
    
    

#Set current nuke script to the first element of the nukeScripts.
setCurrentScript(nukeScripts[0])

print("read path is " + readPath)
nuke.scriptOpen(readPath + '/' + getCurrentScript())



# Recursively render the scripts repeating based on number of interation.
def executeWrite(renderCount):
               
    global renderTimeResults
    
    for i in range(renderCount):
        nuke.execute(name = 'Write1', start = 1, end = framesToRender, incr = 1)
        
        if i == (renderCount - 1):
            jsonResults[getCurrentScript()] = renderTimeResults
            
            averageRenderTime = math.floor(sum(renderTimeResults) / len(renderTimeResults) * 100)/100.0
            # Returns average render time per script tested.
            print("Finished rendering " + getCurrentScript() + " with an average render time of " + str(averageRenderTime) + " seconds")
            updateJSON(jsonResults)

            renderTimeResults = []
            
            currentScriptIndex = nukeScripts.index(getCurrentScript())
            if currentScriptIndex + 1 < len(nukeScripts):
                
                setCurrentScript(nukeScripts[currentScriptIndex + 1])
                executeWrite(renderCount)
                


startTime = timer()

def startRender():
    global startTime
    startTime = timer()
    print("Starting rendering " + getCurrentScript())


def endRender():
    renderTimeResults.append(timer() - startTime)
    print("Finished rendering " + getCurrentScript())


# Adding callbacks for time tracking.
nuke.addBeforeRender(startRender)
nuke.addAfterRender(endRender)

# Render the project.
executeWrite(renderCount)
    

