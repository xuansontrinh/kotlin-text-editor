# Minimal Playground (Kotlin) Source Code Editor
This is a simple (Kotlin) source code editor that accepts typing in script and executes it.

The program was written with `Python 3.8` so it is required to have Python 3.x preinstalled on your machine.

## Tested environment
- OS: `Windows 10`
- Screen Resolution: `3840 x 2160`
- Python version: `3.8`

## Installation
- Install `python 3.x`
- Install required python packages with command `pip install -r requirements.txt` where `requirements.txt` is located at `editor/`
- Start up the python script at `editor/main.py` (No building required)

This should be the screen that you see when running the script successfully:
![Starting Screen](demo-images/start.png)

## Features
### Main features
- [x] Has An editor pane and an output pane
- [x] Supports kotlin script execution
- [x] Shows a spinner to indicate that the script is being executed
- [x] Highlights the error with red text and supports navigating to the error position by double-clicking on the location descriptions of the errors.
- [x] Highlights source code syntax using simple regular expressions

### Secondary (supporting) features
- [x] Supports line numbering for editor pane
- [x] Supports basic text manipulation shortcuts on editor pane such as select all, copy, paste, cut.
- [x] Shows line and col index of the cursor position
- [x] Has vertical and horizontal scroll bars for editor pane
- [x] Has the option to clear the output of previous script runs

## Demo images
![Script processing](demo-images/script-processing.png)
![Script done](demo-images/script-done.png)
![Script error](demo-images/script-error.png)
![Shows outputs of previous runs](demo-images/multiple-times.png)