#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0pre on Fri Oct 28 20:55:56 2022
#

version = "alpha-0"
url = "www.github.com/javidominguez/tesseractOCR-miniGUI"

import wx
import os
import webbrowser
import nvdaControllerClient as nvda
from handler import *

from l10n import *
if not language:
	def _(s):
		return s

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class ListContext(wx.Menu):
	def __init__(self, parent):
		super(ListContext, self).__init__()
		self.parent = parent

		if doc.pagelist and self.parent.GetSelection() > 0:
			item_moveUp = wx.MenuItem(self, wx.ID_ANY, _("Move up"))
			self.Append(item_moveUp)
			self.Bind(wx.EVT_MENU, self.action_moveUp, item_moveUp)

		if doc.pagelist and self.parent.GetSelection() < len(self.parent.Items)-1:
			item_moveDown = wx.MenuItem(self, wx.ID_ANY, _("Move down"))
			self.Append(item_moveDown)
			self.Bind(wx.EVT_MENU, self.action_moveDown, item_moveDown)

		if len(doc.pagelist) > 1:
			item_copy = wx.MenuItem(self, wx.ID_ANY, _("Copy"))
			self.Append(item_copy)
			self.Bind(wx.EVT_MENU, self.action_copy, item_copy)

		if len(doc.pagelist) > 1:
			item_cut = wx.MenuItem(self, wx.ID_ANY, _("Cut"))
			self.Append(item_cut)
			self.Bind(wx.EVT_MENU, self.action_cut, item_cut)

		if doc.clipboard:
			item_paste = wx.MenuItem(self, wx.ID_ANY, _("Paste"))
			self.Append(item_paste)
			self.Bind(wx.EVT_MENU, self.action_paste, item_paste)

		item_remove = wx.MenuItem(self, wx.ID_ANY, _("Remove"))
		self.Append(item_remove)
		self.Bind(wx.EVT_MENU, self.action_remove, item_remove)

	def action_remove(self, event):
		index = self.parent.GetSelection()
		doc.pagelist.pop(index)
		doc.flagModified = True if doc.pagelist else False
		self.parent.Clear()
		self.parent.SetItems(["{}: {}".format(n+1, p) for n, p in enumerate([p.name for p in doc.pagelist])])
		try:
			self.parent.SetSelection(index)
		except:
			if doc.pagelist:
				self.parent.SetSelection(len(doc.pagelist)-1)
			else:
				self.parent.parent.parent.text_ctrl.SetValue("")
				self.parent.parent.parent.text_ctrl.SetFocus()
		self.parent.parent.parent.onListItem(event)
		event.Skip()

	def action_moveUp(self, event):
		self.action_cut(event)
		self.parent.SetSelection(self.parent.GetSelection()-1)
		self.action_paste(event)
		event.Skip()

	def action_moveDown(self, event):
		self.action_cut(event)
		self.parent.SetSelection(self.parent.GetSelection()+1)
		self.action_paste(event)
		event.Skip()

	def action_copy(self, event):
		doc.clipboard = (self.parent.GetSelection(), False)
		event.Skip()

	def action_cut(self, event):
		doc.clipboard = (self.parent.GetSelection(), True)
		event.Skip()

	def action_paste(self, event):
		index, remove = doc.clipboard
		page = doc.pagelist[index]
		if remove: doc.pagelist.pop(index)
		index = self.parent.GetSelection()
		doc.pagelist.insert(index, page)
		doc.clipboard = None
		doc.flagModified = True
		self.parent.Clear()
		self.parent.SetItems(["{}: {}".format(n+1, p) for n, p in enumerate([p.name for p in doc.pagelist])])
		self.parent.SetSelection(index)
		self.parent.parent.parent.onListItem(event)
		event.Skip()

class AlertFileExistsDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: AlertFileExistsDialog.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Confirm"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(self, wx.ID_ANY, _("A file with the same name already exists in the specified location; do you want to replace it?"))
		sizer_1.Add(label, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_YES = wx.Button(self, wx.ID_YES, "")
		self.button_YES.SetDefault()
		self.button_YES.SetLabel(_("&Yes"))
		sizer_2.AddButton(self.button_YES)

		self.button_NO = wx.Button(self, wx.ID_NO, "")
		self.button_NO.SetLabel(_("&No"))
		sizer_2.AddButton(self.button_NO)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_YES.GetId())
		self.SetEscapeId(self.button_NO.GetId())

		self.Layout()

		self.button_NO.Bind(wx.EVT_BUTTON, self.onButtonNO)
		# end wxGlade

	def onButtonNO(self, event):  # wxGlade: AlertFileExistsDialog.<event_handler>
		self.Close()
		event.Skip()
# end of class AlertFileExistsDialog
class alertSaveDocumentDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: alertSaveDocumentDialog.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Save changes?"))

		sizer = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(self, wx.ID_ANY, "", style=wx.ALIGN_CENTER_HORIZONTAL)
		label.SetLabelText(_("Do you want to save changes in the document {}").format(doc.name))
		sizer.Add(label, 0, 0, 0)

		sizerButtons = wx.StdDialogButtonSizer()
		sizer.Add(sizerButtons, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_YES = wx.Button(self, wx.ID_YES, "")
		self.button_YES.SetDefault()
		self.button_YES.SetLabel(_("&Yes"))
		sizerButtons.AddButton(self.button_YES)

		self.button_NO = wx.Button(self, wx.ID_NO, "")
		self.button_NO.SetLabel(_("&No"))
		sizerButtons.AddButton(self.button_NO)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		self.button_CANCEL.SetLabel(_("&Cancel"))
		sizerButtons.AddButton(self.button_CANCEL)

		sizerButtons.Realize()

		self.SetSizer(sizer)
		sizer.Fit(self)

		self.SetAffirmativeId(self.button_YES.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()

		self.button_NO.Bind(wx.EVT_BUTTON, self.onButtonNo)
		# end wxGlade

	def onButtonNo(self, event):  # wxGlade: alertSaveDocumentDialog.<event_handler>
		self.Hide()
		event.Skip()
# end of class alertSaveDocumentDialog
class ScanSettingsDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: ScanSettingsDialog.__init__
		kwds["style"] = kwds.get("style", 0)
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Scanner Settings"))

		sizerOptions = wx.BoxSizer(wx.VERTICAL)

		sizer1 = wx.BoxSizer(wx.HORIZONTAL)
		sizerOptions.Add(sizer1, 1, wx.EXPAND, 0)

		self.radioBoxColor = wx.RadioBox(self, wx.ID_ANY, _("Color"), choices=[_("RGB color"), _("Gray scale"), _("Black and white")], majorDimension=1, style=wx.RA_SPECIFY_COLS)
		self.radioBoxColor.SetSelection(0)
		self.radioBoxColor.SetSelection(["RGB","GRAY","BW"].index(config["scanner"]["color"]))
		sizer1.Add(self.radioBoxColor, 0, 0, 0)

		self.radioBoxPPP = wx.RadioBox(self, wx.ID_ANY, _("Resolution"), choices=[_("100"), _("150"), _("300")], majorDimension=1, style=wx.RA_SPECIFY_COLS)
		self.radioBoxPPP.SetSelection(0)
		self.radioBoxPPP.SetStringSelection(config["scanner"]["resolution"])
		sizer1.Add(self.radioBoxPPP, 0, 0, 0)

		sizer2 = wx.BoxSizer(wx.VERTICAL)
		sizerOptions.Add(sizer2, 1, wx.EXPAND, 0)

		self.checkbox = wx.CheckBox(self, wx.ID_ANY, _("Show this dialog every time a page is scanned?"))
		self.checkbox.SetValue(bool(int(config["general"]["showsettings"])))
		sizer2.Add(self.checkbox, 0, 0, 0)

		sizerButtons = wx.StdDialogButtonSizer()
		sizerOptions.Add(sizerButtons, 0, wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, "")
		self.button_OK.SetDefault()
		self.button_OK.SetLabel(_("&OK"))
		sizerButtons.AddButton(self.button_OK)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		self.button_CANCEL.SetLabel(_("&Cancel"))
		sizerButtons.AddButton(self.button_CANCEL)

		sizerButtons.Realize()

		self.SetSizer(sizerOptions)
		sizerOptions.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		# end wxGlade

# end of class ScanSettingsDialog
class MainFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MainFrame.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE | wx.STAY_ON_TOP
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((1000, 800))
		self.SetTitle(_("TesseractOCR"))

		self.pagelistPanel = DialogPanel(parent=self)
		# Menu Bar
		self.frame_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("New... (ctrl+n)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuFileNew, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Open... (ctrl+o)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuFileOpen, item)
		wxglade_tmp_menu.Append(4, _("Save... (control+s)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuFileSave, id=4)
		wxglade_tmp_menu.Append(5, _("Save as... (ctrl+shift+s)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuFileSaveAs, id=5)
		wxglade_tmp_menu_sub = wx.Menu()
		item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, _("Recognized text (ctrl+shift+x)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuExport, item)
		item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, _("Images"), "")
		self.Bind(wx.EVT_MENU, self.onMenuExportImage, item)
		wxglade_tmp_menu.Append(3, _("Export"), wxglade_tmp_menu_sub, "")
		wxglade_tmp_menu_sub = wx.Menu()
		item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, _("Text"), "")
		self.Bind(wx.EVT_MENU, self.onMenuPrintText, item)
		item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, _("Images"), "")
		self.Bind(wx.EVT_MENU, self.onMenuPrintImages, item)
		wxglade_tmp_menu.Append(6, _("Print"), wxglade_tmp_menu_sub, "")
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Scan settings"), "")
		self.Bind(wx.EVT_MENU, self.onMenuSettings, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Close (ctrl+q)"), _("Closes the application"))
		self.Bind(wx.EVT_MENU, self.onMenuClose, item)
		self.frame_menubar.Append(wxglade_tmp_menu, _("File"))
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Load file (ctrl+f)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuGetLoad, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Digitalize image (ctrl+d)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuGetDigitalize, item)
		self.frame_menubar.Append(wxglade_tmp_menu, _("Get"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(1, _("Recognized text"), "", wx.ITEM_RADIO)
		self.Bind(wx.EVT_MENU, self.onMenuViewRecognized, id=1)
		wxglade_tmp_menu.Append(2, _("List of pages"), "", wx.ITEM_RADIO)
		self.Bind(wx.EVT_MENU, self.onMenuViewPagelist, id=2)
		self.frame_menubar.Append(wxglade_tmp_menu, _("View"))
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Documentation"), "")
		self.Bind(wx.EVT_MENU, self.onHelpDoc, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("View on Github"), "")
		self.Bind(wx.EVT_MENU, self.onHelpGithub, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("About..."), "")
		self.Bind(wx.EVT_MENU, self.onHelpAbout, item)
		self.frame_menubar.Append(wxglade_tmp_menu, _("Help"))
		self.SetMenuBar(self.frame_menubar)
		# Menu Bar end
		self.frame_menubar.FindItem(2)[0].Enable(False)
		self.frame_menubar.FindItem(3)[0].Enable(False)
		self.frame_menubar.FindItem(4)[0].Enable(False)
		self.frame_menubar.FindItem(5)[0].Enable(False)
		self.frame_menubar.FindItem(6)[0].Enable(False)

		self.frame_statusbar = self.CreateStatusBar(1)
		self.frame_statusbar.SetStatusWidths([-1])
		# statusbar fields
		frame_statusbar_fields = [_("frame_statusbar")]
		for i in range(len(frame_statusbar_fields)):
			self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)
		self.frame_statusbar.SetStatusText(_("Ready"))

		self.panel = wx.Panel(self, wx.ID_ANY)

		sizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, ""), wx.VERTICAL)

		self.text_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		self.text_ctrl.SetMinSize((800, 600))
		sizer.Add(self.text_ctrl, 0, wx.EXPAND, 0)

		self.panel.SetSizer(sizer)

		self.Layout()

		# end wxGlade

		self.SetTitle("TesseractOCR - {}".format(doc.name))
		self.text_ctrl.SetSize(self.Size-(10,80))
		self.panel.Bind(wx.EVT_SIZE, self.onWindowSize)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
		self.Bind(wx.EVT_TEXT, self.onTextChanges)
		self.pagelistPanel.Bind(wx.EVT_LISTBOX, self.onListItem)

	def onListItem(self, event):
		if doc.pagelist: self.text_ctrl.SetValue(doc.pagelist[self.pagelistPanel.list_box.GetSelection()].recognized)
		event.Skip()

	def onKey(self, event):
		def hotkey(code, control=False, shift=False, alt=False):
			return event.GetKeyCode() == code and event.controlDown == control and event.shiftDown == shift and event.altDown == alt
		if hotkey(81, True): # control+Q
			self.onMenuClose(event)
		elif hotkey(345): # F6
			if self.text_ctrl.HasFocus():
				self.onMenuViewPagelist(event)
				self.frame_menubar.FindItem(2)[0].Check()
			elif self.pagelistPanel.list_box.HasFocus():
				self.onMenuViewRecognized(event)
				self.frame_menubar.FindItem(1)[0].Check()
		elif hotkey(78, True): # control+n
			self.onMenuFileNew(event)
		elif hotkey(79, True): # control+o
			self.onMenuFileOpen(event)
		elif hotkey(83, True): # control+s
			self.onMenuFileSave(event)
		elif hotkey(83, True, True): # control+shift+s
			self.onMenuFileSaveAs(event)
		elif hotkey(70, True): # )control+f
			self.onMenuGetLoad(event)
		elif hotkey(68, True): # control+d
			self.onMenuGetDigitalize(event)
		elif hotkey(88, True, True): # control+shift+x
			if self.frame_menubar.FindItem(3)[0].Enabled:
				self.onMenuExport(event)
		elif hotkey(367, True): # control+pageDown
			self.moveToPage(+1)
		elif hotkey(366, True): # control+pageUp
			self.moveToPage(-1)
		# print("keycode: {}".format(event.GetKeyCode()))
		event.Skip()

	def moveToPage(self, x):
		current = self.pagelistPanel.list_box.GetSelection()
		if current == -1:
			nvda.message(_("The document is empty"))
			return
		total = len(doc.pagelist)
		new = current+x
		if new < 0: new=0
		if new >= total: new = total-1
		self.text_ctrl.SetValue(doc.pagelist[new].recognized)
		self.pagelistPanel.list_box.SetSelection(new)
		nvda.message(_("Page {} of {}").format(new+1, total))


	def onTextChanges(self, event):
		if doc.pagelist:
			self.frame_menubar.FindItem(2)[0].Enable(True)
			self.frame_menubar.FindItem(3)[0].Enable(True)
			self.frame_menubar.FindItem(6)[0].Enable(True)
			if doc.flagModified:
				self.frame_menubar.FindItem(4)[0].Enable(True)
				self.frame_menubar.FindItem(5)[0].Enable(True)
				self.frame_menubar.FindItem(6)[0].Enable(True)
			pageindex = [p.recognized for p in doc.pagelist].index(self.text_ctrl.GetValue().encode())+1
			npages = len(doc.pagelist)
			self.frame_statusbar.PushStatusText(_("Page {} of {}").format(pageindex, npages))
			if doc.flagModified: self.SetTitle("TesseractOCR - *{}".format(doc.name))
		else:
			self.frame_menubar.FindItem(3)[0].Enable(False)
			self.frame_menubar.FindItem(4)[0].Enable(False)
			self.frame_menubar.FindItem(5)[0].Enable(False)
			self.frame_menubar.FindItem(6)[0].Enable(False)
			self.frame_statusbar.PushStatusText(_("Ready"))
			self.SetTitle("TesseractOCR - {}".format(doc.name))
		event.Skip()

	def onWindowSize(self, event):
		self.text_ctrl.SetSize(self.Size-(10,80))
		event.Skip()

	def onMenuViewPagelist(self, event):  # wxGlade: MainFrame.<event_handler>
		if not doc.pagelist:
			nvda.message(_("The document is empty"))
			event.Skip()
			return
		self.pagelistPanel.Show()
		x, y = self.Size-self.pagelistPanel.Size-(5,25)
		self.pagelistPanel.Move(x, y)
		self.pagelistPanel.list_box.SetFocus()
		event.Skip()

	def onMenuViewRecognized(self, event):  # wxGlade: MainFrame.<event_handler>
		self.text_ctrl.SetFocus()
		self.pagelistPanel.Hide()
		event.Skip()

	def onMenuClose(self, event):  # wxGlade: MainFrame.<event_handler>
		if doc.flagModified:
			dlg = alertSaveDocumentDialog(parent=self)
			res = dlg.ShowModal()
			dlg.Destroy()
			if res == wx.ID_CANCEL:
				return
			elif res == wx.ID_YES:
				self.onMenuFileSave(event)
			else:
				self.Close()
		else:
			self.Close()

	def onMenuFileNew(self, event):  # wxGlade: MainFrame.<event_handler>
		if doc.flagModified:
			dlg = alertSaveDocumentDialog(parent=self)
			res = dlg.ShowModal()
			dlg.Destroy()
			if res == wx.ID_CANCEL:
				event.Skip()
				return
			elif res == wx.ID_YES:
				self.onMenuFileSave(event)
		doc.reset()
		self.pagelistPanel.list_box.Clear()
		self.text_ctrl.Clear()
		self.frame_menubar.FindItem(2)[0].Enable(True)
		event.Skip()
	
	def onMenuFileOpen(self, event):  # wxGlade: MainFrame.<event_handler>
		if doc.flagModified:
			dlg = alertSaveDocumentDialog(parent=self)
			res = dlg.ShowModal()
			dlg.Destroy()
			if res == wx.ID_CANCEL:
				event.Skip()
				return
			elif res == wx.ID_YES:
				self.onMenuFileSave(event)
		dlg = wx.FileDialog(
		parent = self,
		message = _("Open document"),
		defaultDir = os.environ["homepath"],
		defaultFile = "",
		wildcard = _("TesseractOCR documents|*.tes"),
		style = wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			doc.open(dlg.Path)
			if doc.pagelist:
				self.pagelistPanel.list_box.SetItems(["{}: {}".format(n+1, p) for n, p in enumerate([p.name for p in doc.pagelist])])
				self.pagelistPanel.list_box.SetSelection(0)
				self.text_ctrl.SetValue(doc.pagelist[0].recognized)
				self.SetTitle("TesseractOCR - {}".format(doc.name))
		dlg.Destroy()
		event.Skip()

	def onMenuFileSave(self, event):  # wxGlade: MainFrame.<event_handler>
		if doc.flagModified:
			if doc.savedDocumentPath:
				doc.save(doc.savedDocumentPath)
				self.SetTitle("TesseractOCR - {}".format(doc.name))
				nvda.message(_("Document saved"))
			else:
				self.onMenuFileSaveAs(event)
		event.Skip()

	def onMenuFileSaveAs(self, event):  # wxGlade: MainFrame.<event_handler>
		dlg = wx.FileDialog(
		parent = self,
		message = _("Save document"),
		defaultDir = os.environ["homepath"],
		defaultFile = doc.name+".tes",
		wildcard = _("TesseractOCR documents|*.tes"),
		style = wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			if os.path.exists(dlg.Path):
				dlgConfirm = AlertFileExistsDialog(parent=self)
				r = dlgConfirm.ShowModal()
				if r  == wx.ID_YES:
					doc.save(dlg.Path)
				dlgConfirm.Destroy()
			else:
				doc.save(dlg.Path)
		dlg.Destroy()
		self.SetTitle("TesseractOCR - {}".format(doc.name))
		event.Skip()

	def onMenuGetLoad(self, event):  # wxGlade: MainFrame.<event_handler>
		dlg = wx.FileDialog(
		parent = self,
		message = _("Load image"),
		defaultDir = os.environ["homepath"],
		defaultFile = "",
		wildcard = "",
		style = wx.FD_OPEN)
		r = None
		if dlg.ShowModal() == wx.ID_OK:
			r = doc.recognize(dlg.Path)
		dlg.Destroy()
		if r:
			self.text_ctrl.SetValue(_("Recognition failed\n\n")+r.decode("ansi"))
			print(r)
		else:
			self.text_ctrl.SetValue(doc.pagelist[-1].recognized)
			self.pagelistPanel.list_box.Append("{}: {}".format(len(doc.pagelist), doc.pagelist[-1].name))
			self.pagelistPanel.list_box.SetSelection(
			len(self.pagelistPanel.list_box.Items)-1)
		event.Skip()

	def onMenuGetDigitalize(self, event):  # wxGlade: MainFrame.<event_handler>
		if bool(int(config["general"]["showsettings"])):
			if not self.onMenuSettings(event): return
		r = doc.digitalize()
		if r:
			self.text_ctrl.SetValue(_("Recognition failed\n\n")+r.decode("ansi"))
			print(r)
		else:
			self.text_ctrl.SetValue(doc.pagelist[-1].recognized)
			self.pagelistPanel.list_box.Append("{}: {}".format(len(doc.pagelist), doc.pagelist[-1].name))
			self.pagelistPanel.list_box.SetSelection(
				len(self.pagelistPanel.list_box.Items)-1)
		event.Skip()
	def onMenuSettings(self, event):  # wxGlade: MainFrame.<event_handler>
		dlg = ScanSettingsDialog(parent=self)
		if dlg.ShowModal() == wx.ID_OK:
			print ("save configs")
			config["general"]["showsettings"] = 1 if dlg.checkbox.GetValue() else 0
			config["scanner"]["color"] = ["RGB","GRAY","BW"][dlg.radioBoxColor.GetSelection()]
			config["scanner"]["resolution"] = dlg.radioBoxPPP.GetStringSelection()
			config.write()
			dlg.Destroy()
			return True
		dlg.Destroy()
		return False
		# event.Skip()
	def onMenuExport(self, event):  # wxGlade: MainFrame.<event_handler>
		text = doc.exportText()
		dlg = wx.FileDialog(
		parent = self,
		message = _("Save recognized text"),
		defaultDir = os.environ["homepath"],
		defaultFile = "",
		wildcard = _("Text files|*.txt"),
		style = wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			with open(dlg.Path, "wb") as f:
				f.write(text)
		dlg.Destroy()
		event.Skip()

	def onMenuExportImage(self, event):  # wxGlade: MainFrame.<event_handler>
		dlg = wx.DirDialog(self,
		_("Choose a folder where to save the document images:"), style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			if doc.exportAllImages(dlg.Path):
				wx.MessageBox(_("Images saved successfully"), _("Succes"))
			else:
				wx.MessageBox(_("An error occurred and the images have not been saved"), _("Error"))
		dlg.Destroy()
		event.Skip()
	def onMenuPrintText(self, event):  # wxGlade: MainFrame.<event_handler>
		text = doc.exportText()
		path = os.path.join(doc.tempFiles, "{}.txt".format(doc.name))
		with open(path, "wb") as f:
			f.write(text)
		os.startfile(path, "print")
		event.Skip()
	def onMenuPrintImages(self, event):  # wxGlade: MainFrame.<event_handler>
		wx.MessageBox("Event handler 'onMenuPrintImages' not implemented!", "Building")
		event.Skip()

	def onHelpDoc(self, event):  # wxGlade: MainFrame.<event_handler>
		path = os.path.join(".", "doc", lancode, "readme.html")
		if not os.path.exists(path):
			path = os.path.join(".", "doc", "en", "readme.html")
		try:
			os.startfile(path)
		except:
			wx.MessageBox("File not found", "Error")
		event.Skip()

	def onHelpGithub(self, event):  # wxGlade: MainFrame.<event_handler>
		webbrowser.open(url)
		event.Skip()

	def onHelpAbout(self, event):  # wxGlade: MainFrame.<event_handler>
		wx.MessageBox("Version {}".format(version), _("About"))
		event.Skip()
# end of class MainFrame

class DialogPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		self.parent = kwds["parent"]
		# begin wxGlade: DialogPanel.__init__
		kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.Hide()

		sizer = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(self, wx.ID_ANY, _("Document Pages"))
		sizer.Add(label, 0, 0, 0)

		self.list_box = wx.ListBox(self, wx.ID_ANY, choices=[])
		self.list_box.parent = self
		sizer.Add(self.list_box, 0, 0, 0)

		self.SetSizer(sizer)
		sizer.Fit(self)

		self.Layout()
		# end wxGlade

		self.Bind(wx.EVT_CONTEXT_MENU, self.onListContextMenu, self.list_box)

	def onListContextMenu(self, event):
		self.list_box.PopupMenu(ListContext(self.list_box), self.list_box.GetPosition())
# end of class DialogPanel

class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

# end of class App

if __name__ == "__main__":
	# gettext.install("tesseract") # replace with the appropriate catalog name
	# language = gettext.translation("tesseract", localedir="locale", languages=["es"])
	# language.install()

	app = App(0)
	app.MainLoop()
