import sys
import os.path
import nuke
from timeit import default_timer as timer
from sys import platform
import json
import math
from testing_functions.tests import NukeTest


class RenderTest():
    
    def __init__(self):
        self.framesToRender = 30
        self.renderCount = 3
        
        self._currentScript = ""
        self.readPath = ""
        self.savePath = ""
        self.renderTimeResults = []
        self.jsonResults = {}
        self.startTime = timer()
        self.nukeScripts = []


    # dump json data to the output file:
    def updateJSON(self, data):
        with open(self.savePath, "w") as f:
            json.dump(data, f)


    # Set current .nk script:
    def setCurrentScript(self, newScript):
        self._currentScript
        changed = self._currentScript != (newScript)
        if changed:
            self._currentScript = newScript
            

    def getCurrentScript(self):
        return self._currentScript


    # Recursively render the scripts repeating based on number of interation:
    def executeWrite(self, renderCount):
        # Clear previous script, preventing the GUI popping up:
        nuke.scriptClear()
        
        # Open current script with Nuke:
        nuke.scriptOpen(self.readPath + '/' + self.getCurrentScript())
        
        for i in range(renderCount):
            # Find all Write Nodes within the script and execute:
            writeNodes = [node for node in nuke.allNodes(recurseGroups = True) if node.Class() == 'Write']
            # Check for Write Node presence:
            if writeNodes:
                for node in writeNodes: nuke.execute(node, start = 1, end = self.framesToRender, incr = 1)
            else:
                print("No Write Nodes found in " + getCurrentScript())
            if i == (renderCount - 1):
                # Update JSON file once finished rendering a script:
                self.jsonResults[self.getCurrentScript()] = self.renderTimeResults
                
                averageRenderTime = math.floor(sum(self.renderTimeResults) / len(self.renderTimeResults) * 100)/100.0
                # Returns average render time per script tested:
                print("Finished rendering " + self.getCurrentScript() + " with an average render time of " + str(averageRenderTime) + " seconds")
                self.updateJSON(self.jsonResults)

                self.renderTimeResults = []
                # Update current script index:
                currentScriptIndex = self.nukeScripts.index(self.getCurrentScript())
                if currentScriptIndex + 1 < len(self.nukeScripts):
                    
                    self.setCurrentScript(self.nukeScripts[currentScriptIndex + 1])
                    self.executeWrite(renderCount)
            


    # Begin / End Render Callbacks
    def startRender(self):
        global startTime
        startTime = timer()
        print("Starting rendering " + self.getCurrentScript())


    def endRender(self):
        self.renderTimeResults.append(timer() - startTime)
        print("Finished rendering " + self.getCurrentScript())
        
        
    def run(self):
        test = NukeTest()
        test._checkPlatform

        # .nk directory read path:
        self.readPath = test.checkDirectoryPath(sys.argv[1])

        # JSON file path:
        self.savePath = test.checkJsonFormat(test.checkFilePath(sys.argv[2]))

        self.nukeScripts = test.findNukeScripts(path = self.readPath)

        # Set current nuke script to the first element of the self.nukeScripts:
        self.setCurrentScript(self.nukeScripts[0])

        # Amount of frames to render per render count:
        self.framesToRender = test.checkArgv(index = 3, default = self.framesToRender)

        # Amount of times the script is rerendered:
        self.renderCount = test.checkArgv(index = 4, default = self.renderCount)
        
        # Adding callbacks for time tracking:
        nuke.addBeforeRender(self.startRender)
        nuke.addAfterRender(self.endRender)

        # Render the project:
        self.executeWrite(self.renderCount)
        
        