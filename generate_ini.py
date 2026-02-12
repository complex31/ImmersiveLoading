import os
res = os.walk("output")
paths = []

for r in res:
  for f in r[2]:
    p = (f"{r[0]}/{f}").replace("/", "\\")
    if "DISABLED" not in p and (p.endswith((".png", ".jpg", "jpeg", ".dds"))):
      paths.append(p)

n = len(paths)
constants = f'''[Constants]
global $n_imgs = {n}
global $frame = 0
global persist $curr_img
global $active_bar = 0
global $active_bg = 0
global $active_icon = 0
\n'''

present = '''
[Present]
x185 = $active_bar
y185 = $active_bg
z185 = $active_icon
; set vignette mode below
; 0 = none, 1 = bottom, 2 = top+bottom
x187 = 2
; set vignette strength below, default = 4, use positive integer only to avoid bugs
y187 = 4
post $active_bar = $active_bar - 1
post $active_bg = $active_bg - 1
post $active_icon = $active_icon - 1
post $frame = $frame + 1
if $active_bar == 1
  $curr_img = $frame % $n_imgs
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
if $active_bg >= 1 && $active_icon >= 1
  run = CommandListLSLogin
endif
$active_bg = 2

; -----------------------------------

[TextureOverrideLSLoadBarBiggerHydro]
hash = 29feba14
x186 = 0
y186 = 0.749
z186 = 1
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerCryo]
hash = 19f48cd6
x186 = 0.557
y186 = 1
z186 = 1
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerPyro]
hash = b891661d
x186 = 1
y186 = 0.427
z186 = 0.247
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerDendro]
hash = b53d4fd0
x186 = 0.525
y186 = 0.973
z186 = 0.012
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerGeo]
hash = 91f2d7cc
x186 = 1
y186 = 0.788
z186 = 0.031
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerAnemo]
hash = 0f078b00
x186 = 0.482
y186 = 1
z186 = 0.824
run = CustomShaderLB
$active_icon = 2

[TextureOverrideLSLoadBarBiggerElectro]
hash = 59c10306
x186 = 0.690
y186 = 0.388
z186 = 1
run = CustomShaderLB
$active_icon = 2

; ---------------------------------------

;[TextureOverrideText]
;hash = 45544863
;run = CommandListLS_Text

[TextureOverrideLSInazuma]
hash = f7659a3a
run = CommandListRegionIcon

[TextureOverrideLSMondstadt]
hash = 0e22a02d
run = CommandListRegionIcon

[TextureOverrideLSLiyue]
hash = e215b20a
run = CommandListRegionIcon

[TextureOverrideLSSumeru]
hash = 593c1434
run = CommandListRegionIcon

[TextureOverrideLSDungeon]
hash = 121d3c8f
run = CommandListRegionIcon

[TextureOverrideLSTeapot]
hash = 874fa63b
run = CommandListRegionIcon

[TextureOverrideLSColonnade]
hash = 08b0e6b4
run = CommandListRegionIcon

[TextureOverrideLSDragonspine]
hash = d7b6f066
run = CommandListRegionIcon

[TextureOverrideLSChasm]
hash = 910ff5fe
run = CommandListRegionIcon

[TextureOverrideLSEnkanomiya]
hash = 4869caec
run = CommandListRegionIcon

[TextureOverrideLSNatlan]
hash = 66196151
run = CommandListRegionIcon

[TextureOverrideLSSacredMountain]
hash = bc691e6c
run = CommandListRegionIcon

[TextureOverrideLSBygoneSea]
hash = ce44eeb5
run = CommandListRegionIcon

[TextureOverrideLSNodkrai]
hash = 5352112f
run = CommandListRegionIcon

[TextureOverrideLSFontaine]
hash = 59fed606
run = CommandListRegionIcon

[TextureOverrideLSChenyuVale]
hash = a292accf
run = CommandListRegionIcon

; ---------------------------------------

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
\n'''

resources = [
    "[ResourceLB]\nfilename = loadingbar_2x.dds\n",
    "[ResourceLSLogin]\nfilename = .\\login\\login.jpg\n",
    f"[ResourceLS.0]\nfilename = .\\{paths[0]}\n"
]

commandlist = '''
[CommandListCTO]
if ($active_icon >= 1 || $active_bar >= 1) && $active_bg >= 1
  run = CommandListSkin
endif

[CommandListRegionIcon]
if $active_bar >= 1 && $active_bg >= 1
  handling = skip
endif

[CommandListLSLogin]
handling = skip
this = ResourceLSLogin
run = CustomShaderLS
\n'''

commandlist_cond_prefix = '''[CommandListLS]
handling = skip
if $curr_img == 0
  this = ResourceLS.0'''

commandlist_cond = [
    commandlist_cond_prefix
]


for i in range(1,n):
    resources.append(f"[ResourceLS.{i}]\nfilename = .\\{paths[i]}\n")
    commandlist_cond.append(f"else if $curr_img == {i}\n  this = ResourceLS.{i}")
    
commandlist_cond.append("endif\nrun = CustomShaderLS\n")

inifile = open("mod.ini", "w")
inifile.write(constants)
inifile.write(present)
inifile.write(overrides)
inifile.write(customshader)
inifile.write(commandlist)
inifile.write("\n".join(commandlist_cond))
inifile.write("\n\n; ---------- Resources ---------\n\n")
inifile.write("\n".join(resources))
inifile.close()
