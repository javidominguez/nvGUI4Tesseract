#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0pre on Fri Oct 28 20:55:56 2022
#

import wx
import os
from handler import doc

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode

def _(s):
	return s
# end wxGlade


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
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Save... (control+s)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuFileSave, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Save as... (ctrl+shift+s)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuFileSaveAs, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Close (ctrl+q)"), _("Closes the application"))
		self.Bind(wx.EVT_MENU, self.onMenuClose, item)
		self.frame_menubar.Append(wxglade_tmp_menu, _("File"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(1, _("Recognized text"), "", wx.ITEM_RADIO)
		self.Bind(wx.EVT_MENU, self.onMenuViewRecognized, id=1)
		wxglade_tmp_menu.Append(2, _("List of pages"), "", wx.ITEM_RADIO)
		self.Bind(wx.EVT_MENU, self.onMenuViewPagelist, id=2)
		self.frame_menubar.Append(wxglade_tmp_menu, _("View"))
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Load file (ctrl+f)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuGetLoad, item)
		item = wxglade_tmp_menu.Append(wx.ID_ANY, _("Digitalize image (ctrl+d)"), "")
		self.Bind(wx.EVT_MENU, self.onMenuGetDigitalize, item)
		self.frame_menubar.Append(wxglade_tmp_menu, _("Get"))
		self.SetMenuBar(self.frame_menubar)
		# Menu Bar end

		self.frame_statusbar = self.CreateStatusBar(1)
		self.frame_statusbar.SetStatusWidths([-1])
		# statusbar fields
		frame_statusbar_fields = [_("frame_statusbar")]
		for i in range(len(frame_statusbar_fields)):
			self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)

		self.panel = wx.Panel(self, wx.ID_ANY)

		sizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, ""), wx.VERTICAL)

		self.text_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		self.text_ctrl.SetMinSize((800, 600))
		sizer.Add(self.text_ctrl, 0, wx.EXPAND, 0)

		self.panel.SetSizer(sizer)

		self.Layout()

		# end wxGlade
		self.text_ctrl.SetSize(self.Size-(10,80))
		self.panel.Bind(wx.EVT_SIZE, self.onWindowSize)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

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
		print(event.GetKeyCode())
		event.Skip()

	def onWindowSize(self, event):
		self.text_ctrl.SetSize(self.Size-(10,80))
		event.Skip()

	def onMenuViewPagelist(self, event):  # wxGlade: MainFrame.<event_handler>
		self.pagelistPanel.Show()
		x, y = self.Size-self.pagelistPanel.Size-(5,25)
		self.pagelistPanel.Move(x, y)
		self.pagelistPanel.SetFocus()
		event.Skip()

	def onMenuViewRecognized(self, event):  # wxGlade: MainFrame.<event_handler>
		self.text_ctrl.SetFocus()
		self.pagelistPanel.Hide()
		event.Skip()

	def onMenuClose(self, event):  # wxGlade: MainFrame.<event_handler>
		self.Close()

	def onMenuFileNew(self, event):  # wxGlade: MainFrame.<event_handler>
		print("Event handler 'onMenuFileNew' not implemented!")
		event.Skip()
	def onMenuFileOpen(self, event):  # wxGlade: MainFrame.<event_handler>
		print("Event handler 'onMenuFileOpen' not implemented!")
		event.Skip()
	def onMenuFileSave(self, event):  # wxGlade: MainFrame.<event_handler>
		print("Event handler 'onMenuFileSave' not implemented!")
		event.Skip()
	def onMenuFileSaveAs(self, event):  # wxGlade: MainFrame.<event_handler>
		print("Event handler 'onMenuFileSaveAs' not implemented!")
		event.Skip()
	def onMenuGetLoad(self, event):  # wxGlade: MainFrame.<event_handler>
		dlg = wx.FileDialog(
		parent = self,
		message = _("Load image"),
		defaultDir = os.environ["homepath"],
		defaultFile = "",
		wildcard = "",
		style = wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			r = doc.loadImage(dlg.Path)
		dlg.Destroy()
		if r:
			self.text_ctrl.SetValue(_("Recognition failed\n\n")+r.decode("ansi"))
			print(r)
		else:
			self.text_ctrl.SetValue(doc.pagelist[-1].recognized)
			self.pagelistPanel.list_box.Append(doc.pagelist[-1].name)

		event.Skip()
	def onMenuGetDigitalize(self, event):  # wxGlade: MainFrame.<event_handler>
		print("Event handler 'onMenuGetDigitalize' not implemented!")
		event.Skip()
# end of class MainFrame

class DialogPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: DialogPanel.__init__
		kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.Hide()

		sizer = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(self, wx.ID_ANY, _("Document Pages"))
		sizer.Add(label, 0, 0, 0)

		self.list_box = wx.ListBox(self, wx.ID_ANY, choices=[])
		sizer.Add(self.list_box, 0, 0, 0)

		self.SetSizer(sizer)
		sizer.Fit(self)

		self.Layout()
		# end wxGlade

# end of class DialogPanel

class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

# end of class App

if __name__ == "__main__":
	gettext.install("app") # replace with the appropriate catalog name

	app = App(0)
	app.MainLoop()
