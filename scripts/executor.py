from nuke_tests import render_times
from timeit import default_timer as timer
from sys import platform
import os.path
import sys
import nuke
import math
import json

# Renders each script in a directory repeatedly if Write Nodes are present. Outputs render times to a JSON file in a { 'name': [time] } format.
# Prints an average time of the renders per script. Number of renders can be changed in renderCount for a more consistent average time.

# Invoke script with arguments:
# Nuke -t(i) (0: file: script path) (1: directory: .nk scrips path) (2: file: output JSON path) (3: optional number: number of frames to render (default is 30) in '"number"' format) (4: optional number: number of renders(default is 3) in '"number"' format)

# Perform search on a directory and find nuke scripts
# Render them and record time
# Output JSON with times

scriptRenderTest = render_times.RenderTest()
scriptRenderTest.run()
