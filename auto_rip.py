import os, sys
from pprint import pprint
import subprocess
import logging
from typing import Callable, List
import json
import configparser

from makemkv import MakeMKV, ProgressParser

from Drive import Drive

logging.basicConfig(level=logging.INFO, filemode="w", filename="DVD_AUTO_RIPPER.log")
logger = logging.getLogger(__name__)

ini_config = configparser.ConfigParser()
ini_config.read('settings.ini')

def list_drives() -> List[Drive]:
		"""
		Get a list of drives using WMI
		:return: list of drives
		"""
		proc = subprocess.run(
					args=[
						'powershell',
				   					'-noprofile',
				   					'-command',
				   					'Get-WmiObject -Class Win32_LogicalDisk | Select-Object deviceid,volumename,drivetype | ConvertTo-Json'
					],
					text=True,
					stdout=subprocess.PIPE
		)
		if proc.returncode != 0 or not proc.stdout.strip():
			logger.error('Failed to enumerate drives')
			return []
		devices = json.loads(proc.stdout)

		drive_types = {
			0: 'Unknown',
			1: 'No Root Directory',
			2: 'Removable Disk',
			3: 'Local Disk',
			4: 'Network Drive',
			5: 'Compact Disc',
			6: 'RAM Disk',
		}

		return [Drive(
					letter=d['deviceid'],
					label=d['volumename'],
					drive_type=drive_types[d['drivetype']]
		) for d in devices]

def files(path):
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			yield file

def makemkv(output_dir, drive: Drive, rip_one_title=False):
	try:
		with ProgressParser() as progress:
				makemkv = MakeMKV(drive.letter, progress_handler=progress.parse_progress,
				                  minlength=ini_config['Makemkv']['minlength'])
				title = 0 if rip_one_title else "all"
				makemkv.mkv(0, output_dir=output_dir)
	except KeyboardInterrupt:
		makemkv.kill()



def _makemkv_sys(output_path, drive: Drive, min_length=3600):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	makemkvcon = "C:\\Program Files (x86)\\MakeMKV\\makemkvcon.exe"
	# command = [makemkvcon, f"--minlength={min_length}",
    #         "mkv", f"drive:{drive.letter}", "0", output_path]
	command = [makemkvcon, "mkv", f"drive:{drive.letter}", "all", output_path]
	# "C:\Program Files (x86)\MakeMKV\makemkvcon64.exe" -r info dev:D:\
	# command = [makemkvcon, "-r", "info", "dev:" + drive.letter]
	print(" ".join(command))


def compress_movie_folder(input_folder, output_folder, output_file_type=".mp4", del_raw_rip=True):
	# Danger if output_file_type is mkv problems can occur
	json_preset = ini_config['Handbrake']['json_preset']
	handbrake_cli = ini_config['Handbrake']['handbrakecli']

	for input_file in files(input_folder):
		f_name, exten = os.path.splitext(input_file)

		if exten not in {".mkv", ".mp4"}:
			continue

		input_path = os.path.join(input_folder, input_file)
		output_path = os.path.join(output_folder, f"{f_name}{output_file_type}")
		raw_rip_path = output_path+"_raw"

		os.mkdir(raw_rip_path)
		print(f"{raw_rip_path=}")

		command = [handbrake_cli, "-i", input_path, "--json", json_preset, "-o", output_path]
		subprocess.run(command)

		print(f"{input_file!r}: Done")


def rm_dir(path):
	cwd = os.getcwd()
	if not os.path.exists(path):
		return False
	os.chdir(os.path.join(cwd, path))

	for file in os.listdir():
		print("file = " + file)
		os.remove(file)
	os.chdir(cwd)
	os.rmdir(path)


def rip_dvd(input_drive: Drive):

	if input_drive.label is None:
		raise Exception("There was no Drive inserted")

	logger.info(f'Ripping DVD: {input_drive.letter} {input_drive.label}')

	# Step 1: Make the Rip Folder
	# dvd_rip_folder = os.path.join(os.getcwd(), input_drive.label+"_raw")
	media_folder = ini_config['Output']['rip_location']
	dvd_rip_folder = os.path.join(media_folder, input_drive.label+"_raw")
	logger.debug(f"dvd_rip_folder= {dvd_rip_folder!r}")

	os.mkdir(dvd_rip_folder)
	# Step 2: Rip DVD
	logger.info(f'Ripping {input_drive.label} {input_drive.label} with MakeMKV')
	makemkv(output_dir=dvd_rip_folder, drive=input_drive, rip_one_title=True)

	# Step 3 Eject Disc
	input_drive.eject()

	# Step 4 Make Compressed Folder
	commpressed_folder = os.path.join(media_folder, input_drive.label)
	os.mkdir(commpressed_folder)

	# Step 5 Compress Movie Files
	logger.info(f'Compressing folder: {dvd_rip_folder}')
	compress_movie_folder(input_folder=dvd_rip_folder, output_folder=commpressed_folder)

	# Step 6: Remove rip folder
	rm_dir(dvd_rip_folder)

def rip_dvds(drives: List[Drive]):
	compact_drives = [d for d in drives if d.is_compact_disc]
	logger.debug(f'Connected compact drives: {compact_drives}')
	for drive in compact_drives:
		rip_dvd(drive)


if __name__ == "__main__":
	rip_dvd(list_drives()[1])