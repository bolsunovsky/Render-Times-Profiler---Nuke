# Render Time Profiler for Foundry Nuke ![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

 
* Renders each script in a directory repeatedly if Write Nodes are present. Outputs render times to a JSON file in a { 'name': [time] } format.
* Prints an average time of the renders per script. Number of renders can be changed in renderCount for a more consistent average time.

## Sample Output
https://i.imgur.com/ItlA3AU.png
![Example](https://i.imgur.com/NZw4YDs.png "Last render time followed by an average render time")

## Running

Invoke Python script with arguments:

Nuke -t(i) (0: file: executor.py path) (1: directory: .nk scrips path) (2: file: output JSON path) (3: optional number: number of frames to render (default is 30) in a '"number"' format) (4: optional number: number of renders (default is 3) in a '"number"' format)

`nuke -ti <path>/scripts/executor.py <path> <path>/output.json '"60"' '"5"'`
