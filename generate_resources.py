import os
import shutil
import subprocess
from PIL import Image
import json
from multiprocessing import Process

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
    if img.size[0] > tw:
      img = img.resize((tw, th), Image.LANCZOS)
    return img

def generate_dds(name: str):
    subprocess.run(["texconv.exe", "-f", "BC7_UNORM", "-y", "-sepalpha", "-srgb", "-m", "1", "-o", ".", name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    os.remove(name)

def process(out: str, path: str):
    img = Image.open(path)
    img = modes[mode](img)
    img = img.transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
    outpath = f"output/{out}.{"jpg" if jpg else "png"}"
    img.save(outpath, srgb=False)
    if dds:
        generate_dds(out)

if not os.path.exists("config.json"):
    print("Error: config.json not found")
    exit()

config = json.load(open("config.json", "r"))

input_dirs = config["input_dirs"]
dds = config["format"] == "dds"
jpg = config["format"] == "jpg"
tw, th = config["screen_width"], config["screen_height"]
tr = tw / th
mode = config["mode"]
modes = {
    "fill": fill
}
if mode not in modes:
    print(f"Error: unknown mode, supported modes: {modes.keys}")
    exit()

os.makedirs("output", exist_ok=True)

d_index = 0
processed_paths = set()

for input_dir in input_dirs:
    if not os.path.exists(input_dir):
        print(f"Skipped: input directory not found: {input_dir}")
        continue
    print(f"processing... [{input_dir}]")
    trunc_path = "/".join(input_dir.split("/")[1:])
    os.makedirs(f"output/{trunc_path}", exist_ok=True)
    
    index = 0
    res = os.walk(input_dir)
    paths = []
    for r in res:
        for f in r[2]:
            p = f"{r[0]}/{f}"
            if p not in processed_paths and (p.endswith((".png", ".jpg", "jpeg"))):
                paths.append(p)
                processed_paths.add(p)
    
    for path in paths:
        out = f"{trunc_path}/{(index+1):{0}>4}"
        print(f"{(index+1):{0}>4}/{(len(paths)):{0}>4} : {path}")
        Process(target = process, args= (out,path)).run()
        #process(out, path)
        index += 1
    d_index += 1
    