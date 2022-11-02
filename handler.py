from settings import config
from random import choice
from zipfile import ZipFile, ZIP_DEFLATED
import os
import wx
import subprocess
import pickle

def _(s):
	return s

class Page():
	def __init__(self, name="", imagefile="", recognized=""):
		self.name = name
		self.imagefile = imagefile
		self.recognized = recognized

class DocumentHandler():
	def __del__(self):
		for folder, subfolders, files in os.walk(self.tempFiles):
			for f in files:
				os.remove(os.path.join(folder,f))
		os.rmdir(self.tempFiles)

	def __init__(self):
		self.name = "untitled"
		self.savedDocumentPath = ""
		self.flagModified = False
		self.flagBussy = False
		self.pagelist = []
		self.tempFiles = os.path.join(os.environ["temp"], "tesseract-"+self.__randomizePath())
		os.mkdir(self.tempFiles)

	def __randomizePath(self):
		folder = ""
		for i in range (16):
			folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
		return folder

	def recognize(self, filepath, name=None):
		if not name: name = os.path.basename(filepath)
		recogfile = os.path.join(self.tempFiles, "recognized"+self.__randomizePath())
		command = "{exe} \"{filein}\" \"{fileout}\" --dpi 150 --psm 1 --oem 3 -c tessedit_do_invert=0 quiet".format(
			exe = config["binaries"]["tesseract"],
			filein = filepath,
			fileout = recogfile
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		self.flagBussy = False
		if stderr: return stderr
		with open(recogfile+".txt", "rb") as f:
			text = f.read().decode("ansi").split("\n")
		# Suppression of excess blank lines.
		text = "\n".join(filter(lambda l: len(l.replace(" ", ""))>0, text))
		self.pagelist.append(Page(name, filepath, text.encode("ansi")))
		self.flagModified = True

	def digitalize(self):
		outputFile = os.path.join(self.tempFiles, "image-"+self.__randomizePath()+".jpg")
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
		self.savedDocumentPath = path
		with ZipFile(path, "w") as z:
			pagelist = []
			for page in self.pagelist:
				filename = os.path.basename(page.imagefile)
				pagelist.append((page.name, filename, page.recognized))
				z.write(page.imagefile, filename, compress_type=ZIP_DEFLATED)
			pickfile = os.path.join(self.tempFiles, ".pagelist")
			with open(pickfile, "wb") as f:
				pickle.dump(pagelist, f, pickle.HIGHEST_PROTOCOL)
			z.write(pickfile, ".pagelist", ZIP_DEFLATED)
		self.flagModified = False
		self.name = os.path.splitext(os.path.basename(path))[0]

doc = DocumentHandler()