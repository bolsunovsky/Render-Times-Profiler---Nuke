import sys
import os.path
import nuke
from timeit import default_timer as timer
from sys import platform
import json
import math


# Renders each script in a directory repeatedly if Write Nodes are present. Outputs render times to a JSON file in a { 'name': [time] } format.
# Prints an average time of the renders per script. Number of renders can be changed in renderCount for a more consistent average time.

# Invoke script with arguments:
# Nuke -t(i) (0: file: script path) (1: directory: .nk scrips path) (2: file: output JSON path) (3: optional number: number of frames to render (default is 30) in '"number"' format) (4: optional number: number of renders(default is 3) in '"number"' format)

# Perform search on a directory and find nuke scripts
# Render them and record time
# Output JSON with times

class BaseTest:
    @classmethod
    # Check if path leads to a file:
    def checkFilePath(self, path):
        if os.path.isfile(path):
            return path
        else:
            raise TypeError("Third argument must be a file")


    @classmethod
    # Check if file is of JSON format:
    def checkJsonFormat(cls, path):
        # Split the extension from the path and convert it to lower case:
        fileExtension = extensionOf(path)
        if fileExtension == ".json":
            return path
        else:
            raise TypeError("File must end with .json")


    @classmethod
    # Check if path is to a directory:
    def checkDirectoryPath(cls, path):
        if os.path.isdir(path):
            return path
        else:
            raise TypeError("Second argument must be a directory")
            
    @classmethod
    # Check if command line arguments are assignable else return default value
    def checkArgv(cls, index, default):
        try:
            return int(sys.argv[index].strip('"'))
        except:
            return default

    @classmethod
    # Check if running on a compatible os: TODO: test other platforms...
    def _checkPlatform(cls, platform):
        if platform == "darwin": pass
        else:
            print(platform + " has not been tested yet and is unstable")
        

class NukeTest(BaseTest):

    @classmethod
    # Checks for .nk script presence in the given directory:
    def findNukeScripts(cls, path):
        nukeScripts = [script for script in os.listdir(path) if extensionOf(script) == ".nk"]
        if len(nukeScripts) > 0:
            return nukeScripts
        else:
            raise LookupError("No Nuke scripts found in the directory")
            

# Get file extension
extensionOf = lambda file: os.path.splitext(file)[-1].lower()

# dump json data to the output file:
def updateJSON(data):
    with open(savePath, "w") as f:
        json.dump(data, f)


# Set current .nk script:
def setCurrentScript(newScript):
    global _currentScript
    changed = _currentScript != (newScript)
    if changed:
        _currentScript = newScript
        

def getCurrentScript():
    return _currentScript



# Recursively render the scripts repeating based on number of interation:
def executeWrite(renderCount):
    # Clear previous script, preventing the GUI popping up:
    nuke.scriptClear()
    
    # Open current script with Nuke:
    nuke.scriptOpen(readPath + '/' + getCurrentScript())

               
    global renderTimeResults
    
    for i in range(renderCount):
        # Find all Write Nodes within the script and execute:
        writeNodes = [node for node in nuke.allNodes(recurseGroups = True) if node.Class() == 'Write']
        # Check for Write Node presence:
        if writeNodes:
            for node in writeNodes: nuke.execute(node, start = 1, end = framesToRender, incr = 1)
        else:
            print("No Write Nodes found in " + getCurrentScript())
        if i == (renderCount - 1):
            # Update JSON file once finished rendering a script:
            jsonResults[getCurrentScript()] = renderTimeResults
            
            averageRenderTime = math.floor(sum(renderTimeResults) / len(renderTimeResults) * 100)/100.0
            # Returns average render time per script tested:
            print("Finished rendering " + getCurrentScript() + " with an average render time of " + str(averageRenderTime) + " seconds")
            updateJSON(jsonResults)

            renderTimeResults = []
            # Update current script index:
            currentScriptIndex = nukeScripts.index(getCurrentScript())
            if currentScriptIndex + 1 < len(nukeScripts):
                
                setCurrentScript(nukeScripts[currentScriptIndex + 1])
                executeWrite(renderCount)
                
# --------------------------
# Declarations:

NukeTest()._checkPlatform

# .nk directory read path:
readPath = NukeTest().checkDirectoryPath(sys.argv[1])

# JSON file path:
savePath = NukeTest().checkJsonFormat(NukeTest().checkFilePath(sys.argv[2]))

nukeScripts = NukeTest().findNukeScripts(path = readPath)
renderTimeResults = []
jsonResults = {}
_currentScript = ""

# Set current nuke script to the first element of the nukeScripts:
setCurrentScript(nukeScripts[0])


# Amount of frames to render per render count:
framesToRender = NukeTest().checkArgv(index = 3, default = 15)

# Amount of times the script is rerendered:
renderCount = NukeTest().checkArgv(index = 4, default = 3)

startTime = timer()

# Begin / End Render Callbacks
def startRender():
    global startTime
    startTime = timer()
    print("Starting rendering " + getCurrentScript())


def endRender():
    renderTimeResults.append(timer() - startTime)
    print("Finished rendering " + getCurrentScript())


# Adding callbacks for time tracking:
nuke.addBeforeRender(startRender)
nuke.addAfterRender(endRender)

# Render the project:
executeWrite(renderCount)
    
