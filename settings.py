from configobj import ConfigObj

defaultConfig = {
	"binaries": {
		"tesseract": r".\bin\tesseract\tesseract.exe",
		"wia-cmd-scanner": r".\bin\wia-cmd-scanner\wia-cmd-scanner.exe",
		"xpdf-tools": r".\bin\xpdf-tools\pdftopng.exe"
	}
}

def getConfig():
	config = ConfigObj("tesseracOCR-miniGUI.ini")
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