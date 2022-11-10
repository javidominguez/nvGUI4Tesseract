#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# A part of nvGUI4Tesseract, a light and accessible graphical interface to handle the OCR Tesseract.
# Copyright (C) 2022 Javi Dominguez 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from settings import config
from random import choice
from zipfile import ZipFile, ZIP_DEFLATED
import os
import shutil
import wx
import subprocess
import pickle

from l10n import *
if not language:
	def _(s):
		return s

def decode(string):
	if isinstance(string, str): return string
	if isinstance(string, bytes):
		try:
			string = string.decode("utf8")
		except UnicodeDecodeError:
			string = string.decode("ansi")
	return string

def getTesseractLanguage():
	command = "{} --list-langs".format(config["binaries"]["tesseract"])
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
	stdout, stderr = p.communicate()
	availableLanguages = decode(stdout).split("\r\n")[1:]
	if lancode in languages: return languages[lancode] if languages[lancode] in availableLanguages else "eng"
	return "eng"
tesseractLanguage = getTesseractLanguage()

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
		self.name = _("untitled")
		self.savedDocumentPath = ""
		self.flagModified = False
		self.flagCancelled = False
		self.pagelist = []
		self.clipboard = None
		self.tempFiles = os.path.join(os.environ["temp"], "tesseract-"+self.__randomizePath())
		os.mkdir(self.tempFiles)

	def __randomizePath(self):
		folder = ""
		for i in range (16):
			folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
		return folder

	def isPDF(self, path):
		return True if os.path.splitext(path)[-1].lower() == ".pdf" else False

	def recognizePDF(self, path, feedback=None):
		if self.flagCancelled: return
		basenamePNG = self.__randomizePath()
		basenamePDF = os.path.basename(path)
		command = "{} -r 150 -gray \"{}\" \"{}\"".format(
			config["binaries"]["xpdf-tools"],
			path,
			os.path.join(self.tempFiles, basenamePNG)
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		if stderr:
			return _("Failed to extract pages from file {}").format(basenamePDF)
		errors = []
		for page in filter(lambda f: f.startswith(basenamePNG), os.listdir(self.tempFiles)):
			if self.flagCancelled: return
			numpage = int(os.path.splitext(page)[0].split("-")[1])
			if feedback:
				feedback.SetLabelText(_("page {}").format(numpage))
				if not feedback.Shown:
					feedback.Show()
			pagename = _("{file} page {npage}").format(file=basenamePDF, npage=numpage)
			r = self.recognize(os.path.join(self.tempFiles, page), pagename)
			if r:
				errors.append(_("Failed recognition of page {}").format(numpage))
		return "\n".join(errors) if errors else None

	def recognize(self, filepath, name=None, feedback=None):
		if self.flagCancelled: return
		if self.isPDF(filepath):
			r = self.recognizePDF(filepath, feedback=feedback)
			return r
		if not name: name = os.path.basename(filepath)
		recogfile = os.path.join(self.tempFiles, "recognized"+self.__randomizePath())
		command = "{exe} \"{filein}\" \"{fileout}\" --dpi 150 --psm 1 --oem 3 -c tessedit_do_invert=0 -l {lng} quiet".format(
			exe = config["binaries"]["tesseract"],
			filein = filepath,
			fileout = recogfile,
			lng = tesseractLanguage
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		if stderr: return decode(stderr)
		if self.flagCancelled: return
		with open(recogfile+".txt", "rb") as f:
			text = f.read().decode("ansi").split("\n")
		# Suppression of excess blank lines.
		text = "\n".join(filter(lambda l: len(l.replace(" ", ""))>0, text))
		if not self.flagCancelled:
			self.pagelist.append(Page(name, filepath, text.encode("ansi")))
			self.flagModified = True

	def digitalize(self):
		if self.flagCancelled: return
		outputFile = os.path.join(self.tempFiles, "image-"+self.__randomizePath()+".jpg")
		command = "{} /w 0 /h 0 /dpi {} /color {} /format JPG /output {}".format(
			config["binaries"]["wia-cmd-scanner"],
			config["scanner"]["resolution"],
			config["scanner"]["color"],
			outputFile
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		if self.flagCancelled:
			self.flagModified = False
			return _("Cancelled by user")
		if not os.path.exists(outputFile): return stdout
		if not self.flagCancelled: return self.recognize(outputFile, _("Digitalized image {color} {ppp}").format(
			color = config["scanner"]["color"],
			ppp = config["scanner"]["resolution"]
		))

	def exportText(self):
		return b'\n'.join([page.recognized for page in self.pagelist])

	def save(self, path):
		self.savedDocumentPath = path
		with ZipFile(path, "w") as z:
			pagelist = []
			for page in self.pagelist:
				filename = self.__randomizePath()+os.path.splitext(os.path.basename(page.imagefile))[1]
				pagelist.append((page.name, filename, page.recognized))
				z.write(page.imagefile, filename, compress_type=ZIP_DEFLATED)
			pickfile = os.path.join(self.tempFiles, ".pagelist")
			with open(pickfile, "wb") as f:
				pickle.dump(pagelist, f, pickle.HIGHEST_PROTOCOL)
			z.write(pickfile, ".pagelist", ZIP_DEFLATED)
		self.flagModified = False
		self.name = os.path.splitext(os.path.basename(path))[0]

	def reset(self):
		self.name = _("untitled")
		self.savedDocumentPath = ""
		self.flagModified = False
		self.flagCancelled = False
		self.pagelist = []
		for folder, subfolders, files in os.walk(self.tempFiles):
			for f in files:
				os.remove(os.path.join(folder,f))

	def open(self, path):
		self.reset()
		with ZipFile(path, "r") as z:
			z.extractall(self.tempFiles)
		with open(os.path.join(self.tempFiles, ".pagelist"), "rb") as f:
			pagelist = pickle.load(f)
		self.name = os.path.splitext(os.path.basename(path))[0]
		self.savedDocumentPath = path
		for page in pagelist:
			name, file, recognized = page
			self.pagelist.append(Page(name, os.path.join(self.tempFiles, file), recognized))

	def exportAllImages(self, path):
		folder = os.path.join(path, self.name)
		n = 1
		while os.path.exists(folder):
			folder = os.path.join(path, self.name+" ({})".format(n))
			n = n+1
		try:
			os.mkdir(folder)
		except:
			return False
		n = 1
		for page in self.pagelist:
			name = "{doc} [{pg}]{ext}".format(
				doc = self.name,
				pg = _("page {}").format(n),
				ext = os.path.splitext(os.path.basename(page.imagefile))[1]
			)
			try:
				shutil.copy(page.imagefile, os.path.join(folder, name))
			except:
				return False
			n = n+1
		return True

doc = DocumentHandler()