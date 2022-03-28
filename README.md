# HDR10PlusEditor
A simple editor for editing scenes in a HDR10+ JSON.
Allows only for extending/shortening scenes, not adding/deleting.

# Installation
Open command prompt in the base folder.
Install with "pip"
```bash
python3 -m pip install .
```
## Verify instalation
```bash
HDR10PlusEditor -h
```

# Usage
## Input
`-i` or `--input`
The input is expected to be a valid HDR10+ JSON, some verification is done.
## Output
`-o` or `--output`
Where to save the file, same file will overwrite.
## Scene
`-s` or `--scene`
The scene to edit, starting at 0.
## Adjust
`-a` or `--adjust`
How many frames to add/remove from that scene.
## Help page
```
usage: HDR10PlusEditor [-h] --input INPUT --output OUTPUT --scene SCENE --adjust ADJUST

Add/remove frames from a HDR10+ JSON.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input JSON path.
  --output OUTPUT, -o OUTPUT
                        Output JSON path.
  --scene SCENE, -s SCENE
                        Scene number to apply edits.
  --adjust ADJUST, -a ADJUST
                        How to adjust the scene, positive makes it longer, negative makes it shorter.
```