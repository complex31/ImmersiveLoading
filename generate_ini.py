import os
files = os.listdir("output")
n = len(files)

if (n == 0):
    print("no files, exiting...")
    exit()

constants = f'''[Constants]
global $n_imgs = {n}
global $curr_img = 0
global persist $cursor = 0
global $cursor2 = 1
global $active_bar = 0
global $active_bg = 0
\n'''

present = '''
[Present]
x185 = $active_bar
y185 = $active_bg
; TODO: set vignette mode
z185 = 0
post $active_bar = $active_bar - 1
post $active_bg = $active_bg - 1
if $active_bar == 1
  $curr_img = $cursor // 1
  $cursor = ($cursor + $n_imgs * $cursor2 * 0.318309) % $n_imgs
  $cursor2 = ($cursor2 + ($n_imgs // 2 + 1) * 0.368217) % ($n_imgs // 2 + 1)
endif
\n'''

overrides = '''
[TextureOverrideLSLoad]
hash = 77fe5250
handling = skip
this = ResourceLB
run = CustomShaderLB
$active_bar = 2

[TextureOverrideLS]
hash = b7ff7a6e
if $active_bar >= 1 && $active_bg >= 1
  run = CommandListLS
endif
$active_bg = 2

[ShaderOverrideLS]
hash = f61f9bc2a15bedef
run = CommandListCTO

[ShaderOverrideLB]
hash = 4f8eee47124e933d
run = CommandListCTO
\n'''

customshader = '''
[CustomShaderLB]
vs = 4f8eee47124e933d-vs_replace.txt
draw = from_caller

[CustomShaderLS]
vs = f61f9bc2a15bedef-vs_replace.txt
draw = from_caller

;[CustomShaderVG]
;ps = 04911d8f38cd5d4b-ps_replace.txt
;draw = from_caller

[CommandListCTO]
if $active_bar >= 1 && $active_bg >= 1
  run = CommandListSkin
endif
\n'''

resources = [
    "[ResourceLB]\nfilename = loadingbar_2x.dds\n",
    f"[ResourceLS.0]\nfilename = .\\output\\{files[0]}\n"
]
    
commandlist_cond = [
    "[CommandListLS]",
    "handling = skip",
    "if $curr_img == 0",
    "  this = ResourceLS.0"
]


for i in range(1,n):
    resources.append(f"[ResourceLS.{i}]\nfilename = .\\output\\{files[i]}\n")
    commandlist_cond.append(f"else if $curr_img == {i}\n  this = ResourceLS.{i}")
    
commandlist_cond.append("endif\nrun = CustomShaderLS\n;run = CustomShaderVG\n")

inifile = open("mod.ini", "w")
inifile.write(constants)
inifile.write(present)
inifile.write(overrides)
inifile.write(customshader)
inifile.write("\n".join(commandlist_cond))
inifile.write("\n\n; ---------- Resources ---------\n\n")
inifile.write("\n".join(resources))
inifile.close()
