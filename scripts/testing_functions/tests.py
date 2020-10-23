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
    def checkFilePath(cls, path):
        if os.path.isfile(path):
            return path
        else:
            raise TypeError("Third argument must be a file")
    
    # Get file extension
    @classmethod
    def extensionOf(cls, file):
        return os.path.splitext(file)[-1].lower()

    @classmethod
    # Check if file is of JSON format:
    def checkJsonFormat(cls, path):
        # Split the extension from the path and convert it to lower case:
        fileExtension = BaseTest().extensionOf(path)
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
            print("returning default (" + str(default) + ") for argument " + str(index))
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
        scripts = [script for script in os.listdir(path) if NukeTest().extensionOf(script) == ".nk"]
        if len(scripts) > 0:
            return scripts
        else:
            raise LookupError("No Nuke scripts found in the directory")
