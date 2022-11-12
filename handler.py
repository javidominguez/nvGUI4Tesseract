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

class PageList():
	__pages = []
	__index = -1

	def __init__(self, pages=[]):
		if pages: self.add(pages)
		self.evtDocumentChange = None
		self.EventHandler = None

	def __len__(self):
		return len(self.__pages)

	def __getitem__(self, n):
		return self.__pages[n]

	def add(self, item):
		if isinstance(item, Page):
			self.__pages.append(item)
			self.__index = len(self.__pages)-1
			if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
			return 1
		if isinstance(item, PageList):
			item = item.__pages
		if isinstance(item, list):
			x = len(item)
			for i in range(x):
				if isinstance(item[i], Page):
					self.__pages.append(item[i])
				else:
					raise TypeError("item {} is not a Page object".format(i))
		else:
			raise TypeError("The argument must be a Page object or a list of them.")
		self.__index = len(self.__pages)-1
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		return x

	def append(self, item):
		if not isinstance (item, Page):
			raise TypeError("Only objects of type Page can be appened")
		self.__pages.append(item)
		self.__index = len(self.__pages)-1
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)

	def pop(self, index):
		p = self.__pages.pop(index)
		bottom = len(self.__pages)
		if self.__index > bottom:
			self.__index = bottom
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		return p

	def insert(self, index, item):
		if not isinstance(item, Page):
			raise TypeError("Only Page objects can be inserted.")
		if index < 0 or index > len(self.__pages):
			raise IndexError("Cannot insert into position {}; out of range 0-{}".format(
				index, len(self.__pages)
			))
		self.__pages.insert(index, item)
		self.__index = index
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)

	def setIndex(self, i):
		max = len(self.__pages)-1
		if isinstance(i, int):
			if i<0 or i>max:
				raise IndexError("Index {} out of range 0-{}".format(i, max))
			self.__index = i
			if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		elif isinstance(i, Page):
			self.__index = self.__pages.index(i)
			if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		else:
			raise TypeError("Argument must be type int or Page object.")

	def next(self):
		if self.__index+1 >= len(self.__pages):
			return None
		self.__index = self.__index+1
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		return self.__pages[self.__index]

	def previous(self):
		if self.__index-1 < 0:
			return None
		self.__index = self.__index-1
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		return self.__pages[self.__index]

	def first(self):
		self.__index = 0
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		return self.__pages[0]

	def last(self):
		self.__index = len(self.__pages)-1
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
		return self.__pages[self.__index]

	def clear(self):
		self.__pages = []
		self.__index = -1
		if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)

	@property
	def current(self):
		return self.__pages[self.__index]

	@property
	def index(self):
		return self.__index

	@property
	def names(self):
		return [p.name for p in self.__pages]

	@property
	def files(self):
		return [p.imagefile for p in self.__pages]

	@property
	def recognized(self):
		return [p.recognized for p in self.__pages]

	@property
	def asTuple(self):
		return [(p.name, p.imagefile, p.recognized) for p in self.__pages]

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
		self.pages = PageList()
		self.clipboard = None
		self.tempFiles = os.path.join(os.environ["temp"], "tesseract-"+self.__randomizePath())
		os.mkdir(self.tempFiles)

	def __randomizePath(self):
		folder = ""
		for i in range (16):
			folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
		return folder

	def bind(self, event, handler):
		self.pages.evtDocumentChange = event
		self.pages.EventHandler = handler

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
			self.pages.append(Page(name, filepath, text.encode("ansi")))
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
		return b'\n'.join([page.recognized for page in self.pages])

	def save(self, path):
		self.savedDocumentPath = path
		with ZipFile(path, "w") as z:
			pagelist = []
			for page in self.pages:
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
		self.pages.clear()
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
			self.pages.append(Page(name, os.path.join(self.tempFiles, file), recognized))
			self.pages.first()

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
		for page in self.pages:
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

	@property
	def isEmpty(self):
		return True if len(self.pages) == 0 else False

doc = DocumentHandler()