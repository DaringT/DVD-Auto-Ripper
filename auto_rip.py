import os, sys
import subprocess
import time
import logging
from collections import namedtuple
from dataclasses import dataclass
from platform import system as platform_name
from os import system
import ctypes



@dataclass
class Drive:
	letter: str
	label: str
	drive_type: str

	@property
	def is_removable(self) -> bool:
		return self.drive_type == 'Removable Disk'

	@property
	def is_compact_disc(self) -> bool:
		return self.drive_type == 'Compact Disc'

	def eject(self):
		ctypes.windll.WINMM.mciSendStringW(f"open {self.letter.upper()}: type cdaudio alias {self.letter.lower()}_drive", None, 0, None)
		ctypes.windll.WINMM.mciSendStringW(f"set {self.letter.lower()}_drive door open", None, 0, None)




def makemkv(output_path, disc_letter, min_length=3600):
	if os.path.exists(output_path):
		makemkvcon = "C:\\Program Files (x86)\\MakeMKV\\makemkvcon64.exe"
		command = [makemkvcon, f"--minlength={min_length}", "mkv", f"disc:{disc_letter}", "all", output_path]
		# "C:\Program Files (x86)\MakeMKV\makemkvcon64.exe" -r info dev:D:\
		# command = [makemkvcon, "-r", "info", "dev:" + disc_letter]
		m1 = subprocess.run(command, shell=True, text=True, capture_output=True)

		if m1.returncode != 0:
			return False

		print(m1.stdout)

		error_code = "MSG:5010,0,0,\"Failed to open disc","Failed to open disc\""
		lines = m1.stdout.splitlines()[::-1]
		for line in lines:
			if error_code == line:
				return False
			else:
				return True
	else:
		return False

def handbrake(path, output_path):
	# TODO: get figure out if a TRULY subprocess Failed FOR (MAKEMKV & HBrake)
	if os.path.exists(path):
		handbrake_cli = r"C:\Users\Daren\HandBrakeCLI.exe"
		input = r"C:\Users\Daren\Videos\Testing_files\testmkv.mkv"
		json_preset = r"C:\Users\Daren\Documents\preset Handbrake custom.json"

		command = [handbrake_cli, "-i", input, "--json", json_preset, output_path]
		# command = ["echo", "hello"]

		h1 = subprocess.run(command, shell=True, text=True, capture_output=True)
		print(f"{h1.returncode = }")
		print(f"{h1.stdout = }")

		if h1.returncode != 0:
			return False

	else:
		return False

def rip_dvd(input_drive: Drive):
	# Danger This is a just a WROUGHT Script
	# 1: Make WATCH DOG
	# todo 2: Get DVD DATA
	# Todo 3: Need to Movie Metadata
	# TODO 4: Need to dynamically make the rip dir
	# 5: get figure out if a TRULY subprocess Failed FOR (MAKEMKV & HBrake)
	raw_mkv_output = input_drive.label+"_mkv_raw"
	handbrake_output = str

	if makemkv(output_path=raw_mkv_output ,disc_letter=input_drive.letter):
		if handbrake(raw_mkv_output, output_path=handbrake_output):
			return True
		else: return False
	else: return False

if __name__ == "__main__":
	# makemkv(output_path="test", disc_letter="D:\\")
	# main()
	# makemkv()
	pass