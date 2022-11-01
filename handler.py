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
	def __del__(self):
		for folder, subfolders, files in os.walk(self.documentPath):
			for f in files:
				os.remove(os.path.join(folder,f))
		os.rmdir(self.documentPath)

	def __init__(self):
		self.name = "New document"
		self.savedPath = ""
		self.flagModified = False
		self.flagBussy = False
		self.pagelist = []
		self.pageIndex = 0
		self.documentPath = os.path.join(os.environ["temp"], "tesseract-"+self.__randomizePath())
		os.mkdir(self.documentPath)

	def __randomizePath(self):
		folder = ""
		for i in range (16):
			folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
		return folder

	def recognize(self, filepath, name=None):
		if not name: name = os.path.split(filepath)[-1]
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
		with open(os.path.join(self.documentPath, name+".recognized.txt"), "rb") as f:
			text = f.read().decode("ansi").split("\n")
		# Suppression of excess blank lines.
		text = "\n".join(filter(lambda l: len(l.replace(" ", ""))>0, text))
		self.pagelist.append(Page(name, filepath, text.encode("ansi")))
		self.flagModified = True

	def digitalize(self):
		outputFile = os.path.join(self.documentPath, "image-"+self.__randomizePath()+".jpg")
		command = "{} /w 0 /h 0 /dpi {} /color {} /format JPG /output {}".format(
			config["binaries"]["wia-cmd-scanner"],
			config["scanner"]["resolution"],
			config["scanner"]["color"],
			outputFile
		)
		print(command)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		if not os.path.exists(outputFile): return stdout
		return self.recognize(outputFile, _("Digitalized image {color} {ppp}").format(
			color = config["scanner"]["color"],
			ppp = config["scanner"]["resolution"]
		))

	def exportText(self):
		return b'\n'.join([page.recognized for page in self.pagelist])

	def saveDocument(self, path):
		print("save document not implemented")
		print(path)
		self.savedPath = path
		self.flagModified = False

doc = DocumentHandler()