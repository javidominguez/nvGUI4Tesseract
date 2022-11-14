#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# A part of nvGUI4Tesseract, a light and accessible graphical interface to handle the OCR Tesseract.
# Copyright (C) 2022 Javi Dominguez 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import pickle
import shutil
import subprocess
from random import choice
from threading import Lock, Thread
from zipfile import ZIP_DEFLATED, ZipFile

import wx

from l10n import *
from settings import config

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

def randomizePath():
	folder = ""
	for i in range (16):
		folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
	return folder

class Page():
	def __init__(self, name="", imagefile="", recognized=""):
		self.name = name
		self.imagefile = imagefile
		self.recognized = recognized

class PageList():
	def __init__(self, pages=[]):
		if pages:
			self.add(pages)
		else:
			self.__pages = []
		self.__index = -1
		self.modified = False
		self.evtDocumentChange = None
		self.EventHandler = None

	def __len__(self):
		return len(self.__pages)

	def __getitem__(self, n):
		return self.__pages[n]
	def copy(self):
		return self.__pages.copy()

	def add(self, item, flagModified=True):
		if isinstance(item, Page):
			self.__pages.append(item)
			self.__index = len(self.__pages)-1
			if self.EventHandler and self.evtDocumentChange: wx.PostEvent(self.EventHandler, self.evtDocumentChange)
			self.modified = flagModified
			return 1
		if isinstance(item, PageList):
			item = item.__pages
		if isinstance(item, list):
			x = len(item)
			for i in range(x):
				if isinstance(item[i], Page):
					self.__pages.append(item[i])
					self.modified = flagModified
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
		self.modified = True

	def pop(self, index):
		p = self.__pages.pop(index)
		self.modified = True
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
		self.modified = True
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
		self.modified = False
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
		for folder, subfolders, files in os.walk(self.__tempFiles):
			for f in files:
				os.remove(os.path.join(folder,f))
		os.rmdir(self.__tempFiles)

	def __init__(self):
		self.__name = _("untitled")
		self.__savedDocumentPath = ""
		self.pages = PageList()
		self.clipboard = None
		self.__tempFiles = os.path.join(os.environ["temp"], "tesseract-"+randomizePath())
		os.mkdir(self.__tempFiles)
		self.subprocess = None

	def bind(self, event, handler):
		self.pages.evtDocumentChange = event
		self.pages.EventHandler = handler

	def getNewPages(self, source="scanner", eventTerminate=None, eventFeedback=None, eventHandler=None):
		self.subprocess = ProcessNewPages(source, eventTerminate=eventTerminate, eventFeedback=eventFeedback, eventHandler=eventHandler, tempFiles=self.__tempFiles)
		self.subprocess.start()

	def stopSubprocess(self):
		if self.subprocess and self.subprocess.isAlive():
			self.subprocess.kill()

	def pullNewPages(self):
		if self.subprocess:
			self.pages.add(self.subprocess.push())

	def exportText(self):
		return b'\n'.join(self.pages.recognized)

	def exportAllImages(self, path):
		folder = os.path.join(path, self.__name)
		n = 1
		while os.path.exists(folder):
			folder = os.path.join(path, self.__name+" ({})".format(n))
			n = n+1
		try:
			os.mkdir(folder)
		except:
			return False
		n = 1
		for page in self.pages:
			name = "{doc} [{pg}]{ext}".format(
				doc = self.__name,
				pg = _("page {}").format(n),
				ext = os.path.splitext(os.path.basename(page.imagefile))[1]
			)
			try:
				shutil.copy(page.imagefile, os.path.join(folder, name))
			except:
				return False
			n = n+1
		return True

	def open(self, path):
		self.clear()
		with ZipFile(path, "r") as z:
			z.extractall(self.__tempFiles)
		with open(os.path.join(self.__tempFiles, ".pagelist"), "rb") as f:
			pagelist = pickle.load(f)
		self.__name = os.path.splitext(os.path.basename(path))[0]
		self.__savedDocumentPath = path
		self.pages.add([Page(name, os.path.join(self.__tempFiles, file), recognized) for name, file, recognized in pagelist], flagModified=False)
		self.pages.first()

	def save(self, path):
		self.__savedDocumentPath = path
		with ZipFile(path, "w") as z:
			pagelist = []
			for page in self.pages:
				filename = randomizePath()+os.path.splitext(os.path.basename(page.imagefile))[1]
				pagelist.append((page.name, filename, page.recognized))
				z.write(page.imagefile, filename, compress_type=ZIP_DEFLATED)
			pickfile = os.path.join(self.__tempFiles, ".pagelist")
			with open(pickfile, "wb") as f:
				pickle.dump(pagelist, f, pickle.HIGHEST_PROTOCOL)
			z.write(pickfile, ".pagelist", ZIP_DEFLATED)
		self.pages.modified = False
		self.__name = os.path.splitext(os.path.basename(path))[0]

	def clear(self):
		self.__name = _("untitled")
		self.__savedDocumentPath = ""
		self.flagCancelled = False
		self.pages.clear()
		for folder, subfolders, files in os.walk(self.__tempFiles):
			for f in files:
				os.remove(os.path.join(folder,f))

	@property
	def isEmpty(self):
		return True if len(self.pages) == 0 else False

	@property
	def flagModified(self):
		return self.pages.modified

	@property
	def name(self):
		return self.__name

	@property
	def savedDocumentPath(self):
		return self.__savedDocumentPath

	@property
	def tempFiles(self):
		return self.__tempFiles

class ProcessNewPages(Thread):
	def __init__(self, source="scanner", eventTerminate=None, eventFeedback=None, eventHandler=None, tempFiles="", *args, **kwargs):
		super(ProcessNewPages, self).__init__(*args, **kwargs)
		self.setDaemon(True)
		self.__source = source
		self.__eventTerminate = eventTerminate
		self.__eventFeedback = eventFeedback
		self.__EventHandler = eventHandler
		self.__tempFiles = tempFiles
		self.__subprocess = None
		self.__flagCancel = False
		self.__error = ""
		self.__lockPages = Lock()
		self.pagesCache = PageList()

	def run(self):
		images = []
		if self.__source == "scanner":
			images.extend(self.scan())
		elif os.path.splitext(self.__source)[-1].lower() == ".pdf":
			images.extend(self.extractPagesFromPDF())
		else:
			images.append((self.__source, os.path.basename(self.__source)))
		i = 0
		for file, name in images:
			i = i+1
			if self.__error:
				wx.PostEvent(self.__EventHandler, self.__eventTerminate)
				return
			result = self.recognize(file, name)
			if result and isinstance(result, Page) and not self.__flagCancel:
				self.__lockPages.acquire()
				self.pagesCache.add(result)
				self.__lockPages.release()
				self.__eventFeedback.numpage = i
				wx.PostEvent(self.__EventHandler, self.__eventFeedback)
		wx.PostEvent(self.__EventHandler, self.__eventTerminate)

	def kill(self):
		self.__flagCancel = True
		if self.__subprocess: self.__subprocess.kill()

	def push(self):
		self.__lockPages.acquire()
		p = self.pagesCache.copy()
		self.__lockPages.release()
		return p

	def scan(self):
		if self.__flagCancel:
			return []
		outputFile = os.path.join(self.__tempFiles, "image-"+randomizePath()+".jpg")
		command = "{} /w 0 /h 0 /dpi {} /color {} /format JPG /output {}".format(
			config["binaries"]["wia-cmd-scanner"],
			config["scanner"]["resolution"],
			config["scanner"]["color"],
			outputFile
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		self.__subprocess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = self.__subprocess.communicate()
		if self.__flagCancel:
			return []
		if not os.path.exists(outputFile):
			self.__error = stdout
			return []
		return [(outputFile, _("Digitalized image {color} {ppp}").format(
			color = config["scanner"]["color"],
			ppp = config["scanner"]["resolution"]
		))]

	def extractPagesFromPDF(self):
		if self.__flagCancel:
			return []
		basenamePNG = randomizePath()
		basenamePDF = os.path.basename(self.__source)
		command = "{exe} -r 300 -gray \"{input}\" \"{output}\"".format(
			exe=config["binaries"]["xpdf-tools"],
			input=self.__source,
			output=os.path.join(self.__tempFiles, basenamePNG)
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		self.__subprocess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = self.__subprocess.communicate()
		if self.__flagCancel:
			return []
		if stderr:
			self.__error = _("Failed to extract pages from file {}").format(basenamePDF)
			return []
		images = []
		for page in filter(lambda f: f.startswith(basenamePNG), os.listdir(self.__tempFiles)):
			if self.__flagCancel:
				return images
			numpage = int(os.path.splitext(page)[0].split("-")[1])
			pagename = _("{file} page {npage}").format(file=basenamePDF, npage=numpage)
			images.append((os.path.join(self.__tempFiles, page), pagename, ))
		return images

	def recognize(self, filepath, name):
		if self.__flagCancel:
			return
		recogfile = os.path.join(self.__tempFiles, "recognized"+randomizePath())
		command = "{exe} \"{filein}\" \"{fileout}\" --dpi 150 --psm 1 --oem 3 -c tessedit_do_invert=0 -l {lng} quiet".format(
			exe = config["binaries"]["tesseract"],
			filein = filepath,
			fileout = recogfile,
			lng = tesseractLanguage
		)
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		self.__subprocess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = self.__subprocess.communicate()
		if stderr:
			self.__error = decode(stderr)
			return
		if self.__flagCancel:
			return
		with open(recogfile+".txt", "rb") as f:
			text = f.read().decode("ansi").split("\n")
		# Suppression of excess blank lines.
		text = "\n".join(filter(lambda l: len(l.replace(" ", ""))>0, text))
		return Page(name, filepath, text.encode("ansi"))

	@property
	def error(self):
		return self.__error

	@property
	def flagCancel(self):
		return self.__flagCancel

doc = DocumentHandler()
