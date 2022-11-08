import sys, os 
import markdown
import shutil
from distutils.dir_util import copy_tree
from cx_Freeze import setup, Executable 
base = None
if sys.platform == 'win32':
	base = 'Win32GUI'

build_exe_options = dict(
	build_exe="dist",
	packages = ["configobj", "ctypes"],

	optimize=1,
	include_msvcr=True,
)

executables = [
	Executable('gui.py', base=base, targetName="TesseractOCR")
]

setup(
	name="TesseractOCR",
	version="0.1",
	description="Graphical interface, minimalist and accessible, for text recognition with Tesseract",
	author="Javi Dominguez",
	url="https://www.github.com/javidominguez/tesseractOCR-miniGUI",
	options = {"build_exe": build_exe_options},
	executables=executables
)

for folder, subfolders, files in os.walk(os.path.join(os.getcwd(), "doc")):
	for f in files:
		if os.path.splitext(f)[-1].lower() == ".md":
			input = os.path.join(folder,f)
			output = os.path.splitext(input)[0]+".html"
			markdown.markdownFromFile(input=input, output=output)

dir_add = [
	os.path.join(os.getcwd(), "doc"),
	os.path.join(os.getcwd(), "locale"),
	os.path.join(os.getcwd(), "bin")
]
try:
	copy_tree(dir_add[0], os.path.join(os.getcwd(), "dist", "doc"))
	copy_tree(dir_add[1], os.path.join(os.getcwd(), "dist", "locale"))
	copy_tree(dir_add[2], os.path.join(os.getcwd(), "dist", "bin"))
except:
	pass

try:
	shutil.copyfile(os.path.join(os.getcwd(), "nvdaControllerClient64.dll"), os.path.join(os.getcwd(), "dist", "nvdaControllerClient64.dll"))
	shutil.copyfile(os.path.join(os.getcwd(), "nvdaControllerClient32.dll"), os.path.join(os.getcwd(), "dist", "nvdaControllerClient32.dll"))
except:
	pass
