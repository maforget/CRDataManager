import System
import System.Drawing
import System.Windows.Forms
import dmClasses

from System.Drawing import *
from System.Windows.Forms import *
from System import DateTime
from dmClasses import *

import dmGlobals
from dmGlobals import *
from iniReadWrite import *

class runProcess(Form):
    def __init__(self, books, collection):
        self.InitializeComponent()
        self.Icon = Icon(dmGlobals.ICON_SMALL)
        self.Books = books
        self.Collection = collection
        self.TotalRulesets = 0
        self.countRuleset = 0
        self.BookReport = ''
        pass
        
    def InitializeComponent(self):
        self._progressBar1 = System.Windows.Forms.ProgressBar()
        self._btnCancel = System.Windows.Forms.Button()
        self._bgwProcess = System.ComponentModel.BackgroundWorker()
        self._label1 = System.Windows.Forms.Label()
        self._label2 = System.Windows.Forms.Label()
        self._textBox1 = System.Windows.Forms.RichTextBox()
        self._Panel1 = System.Windows.Forms.Panel()
        self._Panel2 = System.Windows.Forms.Panel()
        self._treeView1 = System.Windows.Forms.TreeView()
        self._splitContainer1 = System.Windows.Forms.SplitContainer()
        self._Panel1.SuspendLayout()
        self._splitContainer1.BeginInit()
        self._splitContainer1.Panel1.SuspendLayout()
        self._splitContainer1.Panel2.SuspendLayout()
        self._splitContainer1.SuspendLayout()
        self.SuspendLayout()
        # 
        # progressBar1
        # 
        self._progressBar1.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._progressBar1.Location = System.Drawing.Point(4, 30)
        self._progressBar1.Name = "progressBar1"
        self._progressBar1.Size = System.Drawing.Size(1162, 30)
        self._progressBar1.TabIndex = 0
        # 
        # btnCancel
        # 
        self._btnCancel.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right
        self._btnCancel.Location = System.Drawing.Point(1051, 597)
        self._btnCancel.Name = "btnCancel"
        self._btnCancel.Size = System.Drawing.Size(105, 22)
        self._btnCancel.TabIndex = 1
        self._btnCancel.Text = "Cancel"
        self._btnCancel.UseVisualStyleBackColor = True
        self._btnCancel.Click += self.BtnCancelClick
        # 
        # bgwProcess
        # 
        self._bgwProcess.WorkerReportsProgress = True
        self._bgwProcess.WorkerSupportsCancellation = True
        self._bgwProcess.DoWork += self.BgwProcessDoWork
        self._bgwProcess.ProgressChanged += self.BgwProcessProgressChanged
        self._bgwProcess.RunWorkerCompleted += self.BgwProcessRunWorkerCompleted
        # 
        # label1
        # 
        self._label1.Location = System.Drawing.Point(4, 5)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(252, 23)
        self._label1.TabIndex = 2
        self._label1.Text = "Processing book 0 of 0"
        self._label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._label1.UseMnemonic = False
        # 
        # label2
        # 
        self._label2.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
        self._label2.Location = System.Drawing.Point(914, 5)
        self._label2.Name = "label2"
        self._label2.Size = System.Drawing.Size(252, 23)
        self._label2.TabIndex = 2
        self._label2.Text = "Processing book 0 of 0"
        self._label2.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        self._label2.UseMnemonic = False
        # 
        # textBox1
        # 
        self._textBox1.BackColor = System.Drawing.SystemColors.Window
        self._textBox1.BorderStyle = System.Windows.Forms.BorderStyle.None
        self._textBox1.Dock = System.Windows.Forms.DockStyle.Fill
        self._textBox1.Location = System.Drawing.Point(10, 10)
        self._textBox1.Margin = System.Windows.Forms.Padding(10)
        self._textBox1.Name = "textBox1"
        self._textBox1.ReadOnly = True
        self._textBox1.Size = System.Drawing.Size(711, 497)
        self._textBox1.TabIndex = 3
        self._textBox1.Text = ""
        # 
        # Panel1
        # 
        self._Panel1.Controls.Add(self._label2)
        self._Panel1.Controls.Add(self._progressBar1)
        self._Panel1.Controls.Add(self._label1)
        self._Panel1.Dock = System.Windows.Forms.DockStyle.Top
        self._Panel1.Location = System.Drawing.Point(0, 0)
        self._Panel1.Name = "Panel1"
        self._Panel1.Size = System.Drawing.Size(1168, 68)
        self._Panel1.TabIndex = 0
        # 
        # Panel2
        # 
        self._Panel2.BackColor = System.Drawing.SystemColors.Window
        self._Panel2.Controls.Add(self._textBox1)
        self._Panel2.Dock = System.Windows.Forms.DockStyle.Fill
        self._Panel2.Location = System.Drawing.Point(0, 0)
        self._Panel2.Name = "Panel2"
        self._Panel2.Padding = System.Windows.Forms.Padding(10)
        self._Panel2.Size = System.Drawing.Size(731, 517)
        self._Panel2.TabIndex = 0
        # 
        # treeView1
        # 
        self._treeView1.Dock = System.Windows.Forms.DockStyle.Fill
        self._treeView1.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
        self._treeView1.Location = System.Drawing.Point(0, 0)
        self._treeView1.Name = "treeView1"
        self._treeView1.Size = System.Drawing.Size(427, 517)
        self._treeView1.TabIndex = 4
        self._treeView1.NodeMouseClick += self.NodeClicked
        # 
        # splitContainer1
        # 
        self._splitContainer1.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._splitContainer1.Location = System.Drawing.Point(4, 74)
        self._splitContainer1.Name = "splitContainer1"
        # 
        # splitContainer1.Panel1
        # 
        self._splitContainer1.Panel1.Controls.Add(self._treeView1)
        # 
        # splitContainer1.Panel2
        # 
        self._splitContainer1.Panel2.Controls.Add(self._Panel2)
        self._splitContainer1.Size = System.Drawing.Size(1162, 517)
        self._splitContainer1.SplitterDistance = 427
        self._splitContainer1.TabIndex = 5
        # 
        # runProcess
        # 
        self.ClientSize = System.Drawing.Size(1168, 631)
        self.Controls.Add(self._splitContainer1)
        self.Controls.Add(self._Panel1)
        self.Controls.Add(self._btnCancel)
        self.Name = "runProcess"
        self.Text = "runProcess"
        self.Shown += self.RunProcessShown
        self._Panel1.ResumeLayout(False)
        self._splitContainer1.Panel1.ResumeLayout(False)
        self._splitContainer1.Panel2.ResumeLayout(False)
        self._splitContainer1.EndInit()
        self._splitContainer1.ResumeLayout(False)
        self.ResumeLayout(False)

    def BgwProcessDoWork(self, sender, e):
        collection = e.Argument[0]
        books = e.Argument[1]

        count = 0
        bookTouchCount = 0
        fieldTouchCount = 0

        userVariables = Dictionary[str,str]()

        strReport = ''

        if System.IO.File.Exists(dmGlobals.LOGFILE):
            System.IO.File.Delete(dmGlobals.LOGFILE)

        dtStart = System.DateTime.Now
        dmGlobals.WriteStartTime()

        while count < len(books) and  not self._bgwProcess.CancellationPending:
            tmpDic = dmGlobals.CreateBookDict(books[count])
            if not self._bgwProcess.CancellationPending:
                self._bgwProcess.ReportProgress((100.0 / len(books)) * count + 1, [count, books[count]])
                if dmGlobals.TraceGeneralMessages: print 'Processing Ruleset Collection'
                try:
                    bookReport, detailedReports = collection.ProcessBook(books[count], self._bgwProcess)
                except Exception as er:
                    #report errors instead
                    strError = 'Book: ' + books[count].CaptionWithoutTitle + ' had an unexpected error occured when processing it' + System.Environment.NewLine
                    strError += '    Error: ' + er.message + System.Environment.NewLine
                    self.BookReport += strError
                if self.BookReport != '' or self.BookReport != None:
                    strReport = dmGlobals.AppendReport(strReport, self.BookReport)
                    bookTouchCount = bookTouchCount + 1
                    fieldTouchCount = fieldTouchCount + dmGlobals.GetTouchCount(books[count], tmpDic)
                    if ReadKeyAsBool(dmGlobals.USERINI,  'WriteDataManagerProcessed'):
                       books[count].SetCustomValue('DataManager.processed', DateTime.Now.ToString('yyyy-MM-dd HH:mm:ss'))

            count = count + 1
            self.BookReport = ''

        #add touch count to log
        strReport = strReport + System.Environment.NewLine + System.Environment.NewLine + bookTouchCount.ToString() + ' Books were modified. ' + fieldTouchCount.ToString() + ' Values were changed'
        self._bgwProcess.ReportProgress(100, [count, strReport])
                
        #write out report
        if strReport != '':
            System.IO.File.WriteAllText(dmGlobals.LOGFILE, strReport)
        
        dmGlobals.WriteEndTime()
        duration = System.DateTime.Now - dtStart
        strDuration = duration.ToString('hh\:mm\:ss\.ffff')
        dmGlobals.WriteDurationtime(strDuration)

    def BgwProcessProgressChanged(self, sender, e):
        progress = e.ProgressPercentage
        self.SetProgress(progress, e.UserState)
    
    def SetProgress(self, progress, userState):
        if self.InvokeRequired:
            self.Invoke(self.SetProgress, [progress, userState])
            return

        if progress < 0:
            self.AddToTreeView(userState)
        else:
            count = userState[0]
            booklen = len(self.Books)
            self._progressBar1.Value = progress
            if not isinstance(userState[1], str): self._label2.Text = userState[1].CaptionWithoutTitle
            self._label1.Text = 'Processing ' + count.ToString() + ' of ' + booklen.ToString() + ' books'

    def AddToTreeView(self, userState):
        book = userState[0]
        bookReport = userState[1]
        detailedReports = userState[2]

        if detailedReports:
            bookNode = self._treeView1.Nodes[book.Id.ToString()]

            if not bookNode:
                bookNode = TreeNode(book.CaptionWithoutTitle)
                bookNode.Name = book.Id.ToString()

            for reportType, name, report in detailedReports:
                str = reportType + ": " + name
                bookReport += report
                tn = TreeNode(str)
                tn.Name = book.CaptionWithoutTitle + str
                tn.NodeFont = Font(self._treeView1.Font, FontStyle.Regular)
                tn.Tag = report
                bookNode.Nodes.Add(tn)
                # bookNode.Expand()

            self.BookReport += bookReport
            self._treeView1.Nodes.Add(bookNode)

    def BtnCancelClick(self,sender, e):
        if self._bgwProcess.IsBusy:
            self._bgwProcess.CancelAsync()
        else:
            self.Close()

    def NodeClicked(self,sender, e):
        self._textBox1.Text = ""
        if len(e.Node.Nodes) > 0:
            for x in e.Node.Nodes:
                self._textBox1.Text += x.Tag + System.Environment.NewLine
                pass
        else:
            self._textBox1.Text = e.Node.Tag

    def BgwProcessRunWorkerCompleted(self, sender, e):
        self._btnCancel.Text = 'Close'

    def RunProcessShown(self, sender, e):
        if len(self.Books) > 0:
            self._btnCancel.Text = 'Cancel'
            if self._btnCancel.Click == None:
                self._btnCancel.Click += self.BtnCancelClick
            self._bgwProcess.RunWorkerAsync([self.Collection, self.Books])
        else:
            strMessage = 'The following issues need to be attended to\r\n before you can run Data Manager:'
            strMessage = strMessage + '\r\n no books are selected'
            MessageBox.Show(strMessage, 'Not Enough Info')