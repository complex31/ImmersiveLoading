python .\generate_ini.py
Remove-Item ".\LoadingScreenMod.zip"
$compress = @{
  Path = ".\mod.ini", ".\output", "\*.dds", ".\*_replace.txt"
  DestinationPath = ".\LoadingScreenMod.zip"
}
Compress-Archive @compress
