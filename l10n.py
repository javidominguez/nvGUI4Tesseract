import gettext
import locale

language = None
lancode = locale.normalize(locale.getdefaultlocale()[0].split("_")[0]).split("_")[0]
if gettext.find("tesseract", localedir="locale", languages=[lancode]):
	_ = gettext.gettext
	language = gettext.translation("tesseract", localedir="locale", languages=[lancode])
	language.install()
