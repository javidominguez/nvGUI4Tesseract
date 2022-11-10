#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# A part of nvGUI4Tesseract, a light and accessible graphical interface to handle the OCR Tesseract.
# Copyright (C) 2022 Javi Dominguez 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from configobj import ConfigObj

appname = "TesseractOCR"
author = "Javi Domínguez"
version = "1.0A"
url = "www.github.com/javidominguez/tesseractOCR-miniGUI"

defaultConfig = {
	"general": {
		"showsettings": 1
	},
	"binaries": {
		"tesseract": r".\bin\tesseract\tesseract.exe",
		"wia-cmd-scanner": r".\bin\wia-cmd-scanner\wia-cmd-scanner.exe",
		"xpdf-tools": r".\bin\xpdf-tools\pdftopng.exe"
	},
	"scanner": {
		"color": "GRAY",
		"resolution": "150"
	}
}

def getConfig():
	config = ConfigObj("TesseractOCR.ini")
	flag = False
	for section in defaultConfig:
		if section not in config:
			flag = True
			config[section] = {}
		for key in defaultConfig[section]:
			if key not in config[section]:
				flag = True
				config[section][key] = defaultConfig[section][key]
	if flag:
		try:
			config.write()
		except Exception as inst:
			print("Failed to save configuration file:\n{}".format(inst))
	return config

config = getConfig()