from settings import config
from random import choice
import os

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

	def __randomizePath(self):
		folder = "tesseract-"
		for i in range (16):
			folder = folder+choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
		return os.path.join(os.environ["temp"], folder)

	def load(self, filepath):
		print(filepath)

doc = DocumentHandler()