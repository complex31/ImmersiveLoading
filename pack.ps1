python .\generate_ini.py
Remove-Item ".\LoadingScreenMod.zip"
mkdir ".\Mods\ImmersiveLoading\login"
mkdir ".\ShaderFixes"
Copy-Item -Path ".\mod.ini" -Destination ".\Mods\ImmersiveLoading"
Copy-Item -Path ".\output" -Destination ".\Mods\ImmersiveLoading" -Recurse
Copy-Item -Path ".\login\login.jpg" -Destination ".\Mods\ImmersiveLoading\login\"
Copy-Item -Path ".\*.dds" -Destination ".\Mods\ImmersiveLoading"
Copy-Item -Path ".\*vs_replace.txt" -Destination ".\Mods\ImmersiveLoading"
Copy-Item -Path "..\..\ShaderFixes\04911d8f38cd5d4b-ps_replace.txt" -Destination ".\ShaderFixes"
Copy-Item -Path "..\..\ShaderFixes\4f028a0d23349e1f-ps.txt" -Destination ".\ShaderFixes"
$compress = @{
  Path = ".\Mods", ".\ShaderFixes", "readme.txt"
  DestinationPath = ".\LoadingScreenMod.zip"
}
Compress-Archive @compress
Remove-Item ".\Mods" -Recurse
Remove-Item ".\ShaderFixes" -Recurse