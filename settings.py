from configobj import ConfigObj

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
	config = ConfigObj("TesseractOCR-miniGUI.ini")
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