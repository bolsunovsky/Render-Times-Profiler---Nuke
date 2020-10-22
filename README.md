# Render Time Profiler for Foundry Nuke ![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

 
* Renders each script in a directory repeatedly if Write Nodes are present. Outputs render times to a JSON file in a { 'name': [time] } format.
* Prints an average time of the renders per script. Number of renders can be changed in renderCount for a more consistent average time.


## Running

Invoke Python script with arguments:

Nuke -t(i) (0: file: profiler.py path) (1: directory: .nk scrips path) (2: file: output JSON path) (3: optional number: number of frames to render (default is 30) in '"number"' format) (4: optional number: number of renders(default is 3) in '"number"' format)

`nuke -ti Render-Times-Profiler---Nuke-main/profiler.py Render-Times-Profiler---Nuke-main Render-Times-Profiler---Nuke-main/profilerOutput.json '"60"' '"5"'`
