from settings import config
from random import choice
import os
import wx
import subprocess

class Page():
	def __init__(self, name="", imagefile="", recognized=""):
		self.name = name
		self.imagefile = imagefile
		self.recognized = recognized

class DocumentHandler():
	def __init__(self):
		self.name = "New document"
		self.flagModified = False
		self.flagBussy = False
		self.pagelist = []
		self.pageIndex = 0
		self.documentPath = self.__randomizePath()
		os.mkdir(self.documentPath)

	def __randomizePath(self):
		folder = "tesseract-"
		for i in range (16):
			folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
		return os.path.join(os.environ["temp"], folder)

	def loadImage(self, filepath):
		name = os.path.split(filepath)[-1]
		command = "{exe} \"{filein}\" \"{fileout}\" --dpi 150 --psm 1 --oem 3 -c tessedit_do_invert=0 quiet".format(
			exe = config["binaries"]["tesseract"],
			filein = filepath,
			fileout = os.path.join(self.documentPath, name+".recognized")
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		self.flagBussy = False
		if stderr: return stderr
		with open(os.path.join(self.documentPath, name+".recognized.txt"), "r") as f:
			text = f.readlines()
		# Suppression of excess blank lines.
		text = "\n".join(filter(lambda l: len(l.replace(" ", ""))>1, text))
		self.pagelist.append(Page(name, filepath, text.encode("ansi")))
		self.flagModified = True

doc = DocumentHandler()