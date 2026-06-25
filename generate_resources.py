import os
import shutil
import subprocess
from PIL import Image
import json
from multiprocessing import Pool, cpu_count

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

if not os.path.exists(CONFIG_PATH):
    print(f"Error: config.json not found at: {CONFIG_PATH}")
    exit()

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

input_dirs = config["input_dirs"]
dds = config["format"] == "dds"
jpg = config["format"] == "jpg"
tw, th = config["screen_width"], config["screen_height"]
tr = tw / th
mode = config["mode"]

def fill(img: Image) -> Image:
    width, height = img.size
    ratio = width / height
    if ratio > tr:
        c = width / 2
        img = img.crop((c - height * tr * 0.5, 0, c + height * tr * 0.5, height))
    else:
        c = height / 2
        img = img.crop((0, c - 0.5 * width / tr, width, c + 0.5 * width / tr))
    if img.size[0] > tw:
        img = img.resize((tw, th), Image.LANCZOS)
    return img

modes = {
    "fill": fill
}

if mode not in modes:
    print(f"Error: Unknown mode. Supported modes: {list(modes.keys())}")
    exit()

def generate_dds(output_file_path: str):
    dirname = os.path.dirname(output_file_path)
    subprocess.run(["texconv.exe", "-f", "BC7_UNORM", "-y", "-sepalpha", "-srgb", "-m", "1", "-o", dirname, output_file_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    os.remove(output_file_path)

def process_image(args):
    outpath, path = args  
    try:
        img = Image.open(path)
        img = modes[mode](img)
        img = img.transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
        img.save(outpath, srgb=False)
        if dds:
            generate_dds(outpath)
    except Exception as e:
        print(f"Error processing {path}: {e}")

if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ext = "jpg" if jpg else "png"

    processed_paths = set()
    tasks = []  

    login_input_dir = os.path.join(BASE_DIR, "login")
    if os.path.exists(login_input_dir):
        login_output_dir = os.path.join(login_input_dir, "output")
        os.makedirs(login_output_dir, exist_ok=True)
        for f in os.listdir(login_input_dir):
            if f.lower().startswith("login") and f.lower().endswith((".png", ".jpg", ".jpeg")):
                login_img_path = os.path.join(login_input_dir, f)
                login_out_path = os.path.join(login_output_dir, f"login.{ext}")
                tasks.append((login_out_path, login_img_path))
                processed_paths.add(login_img_path)
                print(f"Processing login image... [{f}]")
                break

    for input_dir in input_dirs:
        if not os.path.isabs(input_dir):
            real_input_path = os.path.join(BASE_DIR, input_dir)
        else:
            real_input_path = input_dir

        if not os.path.exists(real_input_path):
            print(f"Skipped: input directory not found: {input_dir} (Checked at: {real_input_path})")
            continue
        
        print(f"Processing... [{input_dir}]")
        trunc_path = "/".join(input_dir.replace("\\", "/").split("/")[1:])
        os.makedirs(os.path.join(OUTPUT_DIR, trunc_path), exist_ok=True)
        
        index = 0
        res = os.walk(real_input_path)
        paths = []
        for r in res:
            for f in r[2]:
                p = os.path.join(r[0], f)
                if p not in processed_paths and (p.lower().endswith((".png", ".jpg", ".jpeg"))):
                    paths.append(p)
                    processed_paths.add(p)
        
        for path in paths:
            out_file_path = os.path.join(OUTPUT_DIR, trunc_path, f"{(index+1):04d}.{ext}")
            tasks.append((out_file_path, path))
            index += 1

    if tasks:
        cores = cpu_count()
        print(f"\n[+] Found {len(tasks)} images total.")
        print(f"[+] Processing in parallel using {cores} CPU cores...\n")
        
        with Pool(processes=cores) as pool:
            pool.map(process_image, tasks)
            
        print("\n[✓] Done! All images processed successfully.")
    else:
        print("No valid images found in the specified directories.")
