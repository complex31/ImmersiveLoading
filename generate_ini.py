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
global $active_icon = 0
\n'''

present = '''
[Present]
x185 = $active_bar
y185 = $active_bg
z185 = $active_icon
post $active_bar = $active_bar - 1
post $active_bg = $active_bg - 1
post $active_icon = $active_icon - 1
if $active_bar == 1
  $curr_img = $cursor // 1
  $cursor = ($cursor + $n_imgs * $cursor2 * 0.318309) % $n_imgs
  $cursor2 = ($cursor2 + ($n_imgs // 2 + 1) * 0.468217) % ($n_imgs // 2 + 1)
endif
\n'''

overrides = '''
[TextureOverrideLSLoad]
hash = 77fe5250
handling = skip
this = ResourceLB
x186 = 1
y186 = 1
z186 = 1
run = CustomShaderLB
$active_bar = 2

[TextureOverrideLS]
hash = b7ff7a6e
if $active_bar >= 1 && $active_bg >= 1
  run = CommandListLS
endif
$active_bg = 2


[TextureOverrideLSLoadBarBiggerHydro]
hash = 29feba14
x186 = 0
y186 = 0.5
z186 = 1
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerCryo]
hash = 19f48cd6
x186 = 0.7
y186 = 0.8
z186 = 1
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerPyro]
hash = b891661d
x186 = 1
y186 = 0.5
z186 = 0
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerDendro]
hash = b53d4fd0
x186 = 0.5
y186 = 1
z186 = 0
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerGeo]
hash = 91f2d7cc
x186 = 0.8
y186 = 0.8
z186 = 0
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerAnemo]
hash = 0f078b00
x186 = 0
y186 = 0.8
z186 = 0.8
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerElectro]
hash = 59c10306
x186 = 0.5
y186 = 0
z186 = 1
run = CustomShaderLB
$active_icon = 2


[ShaderOverrideLS]
hash = f61f9bc2a15bedef
run = CommandListCTO

[ShaderOverrideLB]
hash = 4f8eee47124e933d
run = CommandListCTO

;[ShaderOverrideVG]
;hash = 04911d8f38cd5d4b
;allow_duplicate_hash = overrule
;run = CommandListCTO

;[ShaderOverrideIcon]
;hash = 4f028a0d23349e1f
;run = CommandListCTO
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

;[CustomShaderIcon]
;ps = 4f028a0d23349e1f-ps_replace.txt
;draw = from_caller

[CommandListCTO]
if ($active_icon >= 1 || $active_bar >= 1) && $active_bg >= 1
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
