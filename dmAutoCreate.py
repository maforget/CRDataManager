
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class dmAutoCreate(Form):
	def __init__(self, books=None):
		self.InitializeComponent()
		self.Books = books
	
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		resources = System.Resources.ResourceManager("dmAutoCreate", System.Reflection.Assembly.GetEntryAssembly())
		self._tscMain = System.Windows.Forms.ToolStripContainer()
		self._ttHelp = System.Windows.Forms.ToolTip(self._components)
		self._tsMain = System.Windows.Forms.ToolStrip()
		self._tsbtnDeleteTemplate = System.Windows.Forms.ToolStripButton()
		self._tsbtnAddTemplate = System.Windows.Forms.ToolStripButton()
		self._splTreeActiveContent = System.Windows.Forms.SplitContainer()
		self._treeView1 = System.Windows.Forms.TreeView()
		self._tsddTemplateSelect = System.Windows.Forms.ToolStripDropDownButton()
		self._defaultToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._tscMain.ContentPanel.SuspendLayout()
		self._tscMain.TopToolStripPanel.SuspendLayout()
		self._tscMain.SuspendLayout()
		self._tsMain.SuspendLayout()
		self._splTreeActiveContent.BeginInit()
		self._splTreeActiveContent.Panel1.SuspendLayout()
		self._splTreeActiveContent.SuspendLayout()
		self.SuspendLayout()
		# 
		# tscMain
		# 
		# 
		# tscMain.ContentPanel
		# 
		self._tscMain.ContentPanel.Controls.Add(self._splTreeActiveContent)
		self._tscMain.ContentPanel.Size = System.Drawing.Size(858, 526)
		self._tscMain.Dock = System.Windows.Forms.DockStyle.Fill
		self._tscMain.Location = System.Drawing.Point(0, 0)
		self._tscMain.Name = "tscMain"
		self._tscMain.Size = System.Drawing.Size(858, 551)
		self._tscMain.TabIndex = 0
		self._tscMain.Text = "toolStripContainer1"
		# 
		# tscMain.TopToolStripPanel
		# 
		self._tscMain.TopToolStripPanel.Controls.Add(self._tsMain)
		# 
		# tsMain
		# 
		self._tsMain.Dock = System.Windows.Forms.DockStyle.None
		self._tsMain.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden
		self._tsMain.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._tsddTemplateSelect,
			self._tsbtnDeleteTemplate,
			self._tsbtnAddTemplate]))
		self._tsMain.Location = System.Drawing.Point(0, 0)
		self._tsMain.Name = "tsMain"
		self._tsMain.Size = System.Drawing.Size(858, 25)
		self._tsMain.Stretch = True
		self._tsMain.TabIndex = 0
		# 
		# tsbtnDeleteTemplate
		# 
		self._tsbtnDeleteTemplate.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
		self._tsbtnDeleteTemplate.Image = resources.GetObject("tsbtnDeleteTemplate.Image")
		self._tsbtnDeleteTemplate.ImageTransparentColor = System.Drawing.Color.Magenta
		self._tsbtnDeleteTemplate.Name = "tsbtnDeleteTemplate"
		self._tsbtnDeleteTemplate.Size = System.Drawing.Size(23, 22)
		self._tsbtnDeleteTemplate.Text = "Delete Template"
		# 
		# tsbtnAddTemplate
		# 
		self._tsbtnAddTemplate.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
		self._tsbtnAddTemplate.Image = resources.GetObject("tsbtnAddTemplate.Image")
		self._tsbtnAddTemplate.ImageTransparentColor = System.Drawing.Color.Magenta
		self._tsbtnAddTemplate.Name = "tsbtnAddTemplate"
		self._tsbtnAddTemplate.Size = System.Drawing.Size(23, 22)
		self._tsbtnAddTemplate.Text = "Add New Template"
		# 
		# splTreeActiveContent
		# 
		self._splTreeActiveContent.Dock = System.Windows.Forms.DockStyle.Fill
		self._splTreeActiveContent.Location = System.Drawing.Point(0, 0)
		self._splTreeActiveContent.Name = "splTreeActiveContent"
		# 
		# splTreeActiveContent.Panel1
		# 
		self._splTreeActiveContent.Panel1.Controls.Add(self._treeView1)
		self._splTreeActiveContent.Size = System.Drawing.Size(858, 526)
		self._splTreeActiveContent.SplitterDistance = 216
		self._splTreeActiveContent.TabIndex = 0
		# 
		# treeView1
		# 
		self._treeView1.Dock = System.Windows.Forms.DockStyle.Fill
		self._treeView1.Location = System.Drawing.Point(0, 0)
		self._treeView1.Name = "treeView1"
		self._treeView1.Size = System.Drawing.Size(216, 526)
		self._treeView1.TabIndex = 0
		# 
		# tsddTemplateSelect
		# 
		self._tsddTemplateSelect.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._defaultToolStripMenuItem]))
		self._tsddTemplateSelect.Name = "tsddTemplateSelect"
		self._tsddTemplateSelect.Size = System.Drawing.Size(75, 22)
		self._tsddTemplateSelect.Text = "Templates"
		# 
		# defaultToolStripMenuItem
		# 
		self._defaultToolStripMenuItem.Name = "defaultToolStripMenuItem"
		self._defaultToolStripMenuItem.Size = System.Drawing.Size(152, 22)
		self._defaultToolStripMenuItem.Text = "Default"
		self._defaultToolStripMenuItem.CheckedChanged += self.TemplateCheckedChanged
		# 
		# dmAutoCreate
		# 
		self.ClientSize = System.Drawing.Size(858, 551)
		self.Controls.Add(self._tscMain)
		self.Name = "dmAutoCreate"
		self.Text = "dmAutoCreate"
		self._tscMain.ContentPanel.ResumeLayout(False)
		self._tscMain.TopToolStripPanel.ResumeLayout(False)
		self._tscMain.TopToolStripPanel.PerformLayout()
		self._tscMain.ResumeLayout(False)
		self._tscMain.PerformLayout()
		self._tsMain.ResumeLayout(False)
		self._tsMain.PerformLayout()
		self._splTreeActiveContent.Panel1.ResumeLayout(False)
		self._splTreeActiveContent.EndInit()
		self._splTreeActiveContent.ResumeLayout(False)
		self.ResumeLayout(False)


	def TemplateCheckedChanged(self, sender, e):
		RefreshPreview()
		pass
	
	def RefreshPreview(self):
		
		pass
	
	def RefreshTemplates(self):
		
		pass