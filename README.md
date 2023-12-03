# DVD Auto Ripper

## About
This a project is a made because I needed a DVD ripping script for ripping DVDs automatically and eject the disc. After, The script will compress the movie files. This script can work with multiple DVD drives synchronously. 

This has a costume watchdog that waits to for a DVD to be inserted. After it rips the DVD by a MakeMKV wrapper library, ejects the Disc via pywin32, After the raw rip folder gets compressed it moves it to your Media Folder. For Handbrake json preset file you can create one from the HandbrakeGUI and overwrite the current one.

## OS Requirements
```
Windows 10
Windows 11 (is untested but should work)
```
## Settings
If you are just ripping Movies and not TV Shows you will want to change the `rip_one_video_file` to **true** and change the `minlength` to **3600** 

```ini
[Makemkv]
rip_one_video_file=false
minlength=1200
del_raw_rip = true

[Handbrake]
; use IP address in case network name resolution is not working
compress_with_Handbrake=true
handbrakecli = C:\Users\Daren\HandBrakeCLI.exe
json_preset = hb_preset_settings.json

[Output]
rip_location = C:\Users\Daren\Videos\Media
```

# Installation

You will need [HandbrakeCli](https://handbrake.fr/downloads2.php) and [MakeMKV](https://www.makemkv.com/) installed. MakeMKV needs to be added the Environment Variables.

## Todo
This script still needs some bugs fixed and I need to figure out how to automate/semi-automate auto renaming Movies and TV Shows. Script also needs to be compatible with Linux.

## Contributing
I am open to improvements. For changes please open an issue to discuss what you would like to change. 