import os
import subprocess
from PIL import Image
import json

def fill(img: Image) -> Image:
    global tw, th, tr
    width, height = img.size
    ratio = width/height
    if ratio > tr:
        c = width / 2
        img = img.crop(( c - height*tr*0.5, 0, c + height*tr*0.5, height))
    else:
        c = height / 2
        img = img.crop((0, c - 0.5*width/tr, width, c + 0.5*width/tr))
    img = img.resize((tw, th), Image.LANCZOS)
    return img

def generate_dds(png: str):
    subprocess.run(["texconv.exe", "-f", "BC7_UNORM", "-y", "-sepalpha", "-srgb", "-m", "1", "-o", ".", png], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    os.remove(png)

if not os.path.exists("input"):
    print("Error: input folder not found")
    exit()
files = [x for x in os.listdir("input") if (x.endswith("png") or x.endswith("jpg") or x.endswith("jpeg"))]
config = json.load(open("config.json", "r"))
dds = config["format"] == "dds"
tw, th = config["screen_width"], config["screen_height"]
tr = tw / th
mode = config["mode"]
modes = {
    "fill": fill
}
if mode not in modes:
    print(f"Error: unknown mode, supported modes: {modes.keys}")
    exit()

index = 0
print("processing... ")
if not os.path.exists("output"):
    os.makedirs("output") 

for file in files:
    print(f"{(index+1):{0}>4}/{(len(files)):{0}>4}")
    img = Image.open(f"./input/{file}")
    img = modes[mode](img)
    png = f"output/{index:{0}>4}.png"
    img.save(png, 'PNG', srgb=False)
    if dds:
        generate_dds(png)
    index += 1
    