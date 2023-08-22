# AMCOE

This is a GUI written in Python for converting the .cli output from a slicer software to a format supported by SST.

## Getting Started

### Prerequisites

python3

```
sudo apt-get install python3
```

pip3

```
sudo apt-get install python3-pip
```

pyopengl

```
sudo apt-get install python3-opengl
```

pyqt5

```
pip3 install pyqt5
sudo apt-get install python3-pyqt5  
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools
```

qdarkstyle

```
pip3 install qdarkstyle
```

## Usage

Run the GUI using 

```
python3 GUI.py
```
Parameters can be modified as double values

Parameters.csv can be saved in a directory, but only a single Parameters.csv file can exist in a directory, and existing file will be *overwritten*

Preheat patterns are configured independantly of the import .cli file.

The file browser only imports .cli files, present in the CLI files directory.

To save the converted file provide an address for the directory, this directory will be *overwritten*.

The preheat patterns are integrated into the save folders, with the bottom plate preheat as layer 0, and layer preheats at the start of every other layer folder.

Parameters.csv for entire build saved in the same directory as the converted file output.

## Features added

### First commit

* File parse and save 
* Functional GUI to display layer
* Sample .cli files.

### Second commit

* Basic error information using a new window prompt

### Third commit

* Dark theme
* Performance optimisations and bug fixes

### Fifth commit

* Modify beam parameters
* Save beam parameters .csv

### Sixth commit

* Per layer parameter modification
* Preheat configurator for base plate and individual layers

### Seventh commit

* Per layer configure pattern parameters 
* Build parameters .csv generation

### Ninth commit

* Label changes
* Updates parameter file

### Tenth commit

* Calibrate tab

## Author

* Sahil Bhandary K
