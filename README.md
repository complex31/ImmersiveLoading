# Loading Screen Mod Generator

## Prerequisites
- Install [Python](https://python.org/downloads)
- Install [Pillow](https://pypi.org/project/pillow/) or use on cmd as admin: pip install pillow

## Setup
- Copy the `ils_generator` folder inside `Mods` folder to your `GIMI/Mods` folder
- Copy the files inside `sf` folder to your `GIMI/ShaderFixes` folder
- Add your images in the input folders, make subfolders as you need
- Create a `login` folder in the root directory and place exactly one image named `login.png` or `login.jpg` inside it
- Set your screen width and height in `config.json`
- Add your input folders names in `config.json`

*Max input subfolders: 99*

*Max images in each subfolder: 9999*

## Usage
- Run `generate_resources.py` to convert images from your input folders into proper aspect ratio and format (saves general backgrounds into `output` and your login image into `login/output`)
- Run `generate_ini.py` to generate 3DMigoto mod INI file according to the processed output images from the previous step
- To skip certain subfolder or image from `output`, add "DISABLED" in the folder name before running the script for generating INI

## Known bugs
- Sometimes during in-game night, the loading screen might show dark color for a few frames. This is likely caused by the shader that darkens/lightens the loading screen based on in-game time, but I haven't figured out how exactly to fix it yet
- Some UI elements and object might display as solid-color patches for a few frames just after the loading screen fades away. Not sure how to fix it yet.