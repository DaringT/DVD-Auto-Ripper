import ctypes
from dataclasses import dataclass


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