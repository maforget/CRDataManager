
import clr
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

clr.AddReference("System.IO")
from System.IO import Directory, Path

import dmGlobals

class frmProfile(Form):
	def __init__(self, folder):
		self.InitializeComponent()
		self._folder = folder
		self._ChosenProfile = dmGlobals.DATFILE
		
	@property
	def ChosenProfile(self):
		return self._ChosenProfile

	@ChosenProfile.setter
	def ChosenProfile(self, value):
		self._ChosenProfile = value
	
	def InitializeComponent(self):
		self._btnOK = System.Windows.Forms.Button()
		self._cbProfile = System.Windows.Forms.ComboBox()
		self._lblProfile = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# btnOK
		# 
		self._btnOK.Location = System.Drawing.Point(250, 39)
		self._btnOK.Name = "btnOK"
		self._btnOK.Size = System.Drawing.Size(75, 23)
		self._btnOK.TabIndex = 0
		self._btnOK.Text = "OK"
		self._btnOK.UseVisualStyleBackColor = True
		self._btnOK.Click += self.BtnOKClick
		# 
		# cbProfile
		# 
		self._cbProfile.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._cbProfile.FormattingEnabled = True
		self._cbProfile.Location = System.Drawing.Point(58, 12)
		self._cbProfile.Name = "cbProfile"
		self._cbProfile.Size = System.Drawing.Size(267, 21)
		self._cbProfile.TabIndex = 1
		# 
		# lblProfile
		# 
		self._lblProfile.Location = System.Drawing.Point(12, 15)
		self._lblProfile.Name = "lblProfile"
		self._lblProfile.Size = System.Drawing.Size(40, 23)
		self._lblProfile.TabIndex = 2
		self._lblProfile.Text = "Profile: "
		# 
		# frmProfile
		# 
		self.ClientSize = System.Drawing.Size(337, 74)
		self.Controls.Add(self._lblProfile)
		self.Controls.Add(self._cbProfile)
		self.Controls.Add(self._btnOK)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.Name = "frmProfile"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "Profile"
		self.Load += self.FrmProfileLoad
		self.ResumeLayout(False)


	def BtnOKClick(self, sender, e):
		chosen = self._cbProfile.SelectedItem
		chosen = "dataman" if chosen == "Default" else chosen
		self.ChosenProfile = Path.Combine(self._folder, chosen + ".dat")
		self.Close()

	def FrmProfileLoad(self, sender, e):
		dat_files = self.enumerate_dat_files(self._folder)
		
		if len(dat_files) > 0:
			self.load_dats(dat_files)
		else:
			self.ChosenProfile = dmGlobals.DATFILE
			self.Close()
		
	def enumerate_dat_files(self, folder_path):
		dat_files = []
		
		files = Directory.EnumerateFiles(folder_path, "*.dat")
		for file in files:
			filename = Path.GetFileNameWithoutExtension(file)
			if filename != "dataman":
				dat_files.Add(filename)
		return dat_files

	def load_dats(self, dat_files):
		self._cbProfile.Items.Clear()
		self._cbProfile.Items.Add("Default")

		for dat in dat_files:
			self._cbProfile.Items.Add(dat)

		self._cbProfile.SelectedIndex = 0