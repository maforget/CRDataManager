import System
import System.Drawing
import System.Windows.Forms
import dmClasses

from System.Drawing import *
from System.Windows.Forms import *
from dmClasses import *

import dmGlobals
from dmGlobals import *

class runProcess(Form):
    def __init__(self, books, collection):
        self.InitializeComponent()
        self.Icon = Icon(dmGlobals.ICON_SMALL)
        self.Books = books
        self.Collection = collection
        self.TotalRulesets = 0
        self.countRuleset = 0
        pass
        
    def InitializeComponent(self):
        self._progressBar1 = System.Windows.Forms.ProgressBar()
        self._btnCancel = System.Windows.Forms.Button()
        self._bgwProcess = System.ComponentModel.BackgroundWorker()
        self._label1 = System.Windows.Forms.Label()
        self._label2 = System.Windows.Forms.Label()
        self._textBox1 = System.Windows.Forms.TextBox()
        self.Panel1 = System.Windows.Forms.Panel()
        self.Panel2 = System.Windows.Forms.Panel()
        self.Panel1.SuspendLayout()
        self.Panel2.SuspendLayout()
        self.SuspendLayout()
        #
        # progressBar1
        #
        self._progressBar1.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._progressBar1.Location = System.Drawing.Point(4, 30)
        self._progressBar1.Name = "progressBar1"
        self._progressBar1.Size = System.Drawing.Size(908, 30)
        self._progressBar1.TabIndex = 0
        #
        # btnCancel
        #
        self._btnCancel.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right
        self._btnCancel.Location = System.Drawing.Point(797, 527)
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
        self._label2.Location = System.Drawing.Point(660, 5)
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
        self._textBox1.Dock = System.Windows.Forms.DockStyle.Fill
        self._textBox1.Location = System.Drawing.Point(0, 0)
        self._textBox1.Multiline = True
        self._textBox1.Name = "textBox1"
        self._textBox1.ReadOnly = True
        self._textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Both
        self._textBox1.Size = System.Drawing.Size(914, 455)
        self._textBox1.TabIndex = 3
        self._textBox1.WordWrap = False
        #
        # Panel1
        #
        self.Panel1.Dock = System.Windows.Forms.DockStyle.Top
        self.Panel1.Controls.Add(self._label2)
        self.Panel1.Controls.Add(self._progressBar1)
        self.Panel1.Controls.Add(self._label1)
        self.Panel1.Location = System.Drawing.Point(0, 0)
        self.Panel1.Size = System.Drawing.Size(914, 68)
        self.Panel1.Name = "Panel1";
        #
        # Panel2
        #
        self.Panel2.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self.Panel2.Controls.Add(self._textBox1)
        self.Panel2.Size = System.Drawing.Size(914, 455)
        self.Panel2.Location = System.Drawing.Point(0, 66);
        self.Panel2.Name = "Panel2";
        self.Panel2.TabIndex = 4
        #
        # runProcess
        #
        self.ClientSize = System.Drawing.Size(914, 561)
        self.Controls.Add(self.Panel1)
        self.Controls.Add(self.Panel2)
        self.Controls.Add(self._btnCancel)
        self.Name = "runProcess"
        self.Text = "runProcess"
        self.Shown += self.RunProcessShown
        self.Panel1.ResumeLayout(False)
        self.Panel2.ResumeLayout(False)
        self.Panel2.PerformLayout()
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

        self.TotalRulesets = self.getTotalNumberOfRuleSet(collection)
        while count < len(books):
            tmpDic  = dmGlobals.CreateBookDict(books[count])
            if not self._bgwProcess.CancellationPending:
                self._bgwProcess.ReportProgress((100 / len(books)) * count + 1, [count, books[count]])
                if dmGlobals.TraceGeneralMessages: print 'Processing Ruleset Collection'
                try:
                    bookReport = collection.ProcessBook(books[count], self._bgwProcess)
                except Exception as er:
                    #report errors instead
                    bookReport = ''
                    strReport = 'Book: ' + books[count].CaptionWithoutTitle + ' had an unexpected error occured when processing it' + System.Environment.NewLine
                    strReport = strReport + '    Error: ' + er.message
                if bookReport != '':
                    strReport = dmGlobals.AppendReport(strReport, bookReport)
                    bookTouchCount = bookTouchCount + 1
                    fieldTouchCount = fieldTouchCount + dmGlobals.GetTouchCount(books[count], tmpDic)
            count = count + 1


        #add touch count to log
        strReport = strReport + System.Environment.NewLine + System.Environment.NewLine + bookTouchCount.ToString() + ' Books were modified. ' + fieldTouchCount.ToString() + ' Values were changed'
        self._bgwProcess.ReportProgress(100, [count, strReport])
                
        #write out report
        if strReport!= '':
            System.IO.File.WriteAllText(dmGlobals.LOGFILE, strReport)
        
        dmGlobals.WriteEndTime()
        duration = System.DateTime.Now - dtStart
        strDuration = duration.ToString('hh\:mm\:ss\.ffff')
        dmGlobals.WriteDurationtime(strDuration)

        pass

    def getTotalNumberOfRuleSet(self, element):
        count = 0

        grp = element.Groups
        ruleSet = element.Rulesets

        if isinstance(ruleSet, list):
            count += len(ruleSet)

        if isinstance(grp, list):
            for each_element in grp:
                count += self.getTotalNumberOfRuleSet(each_element)
        
        return count

    def BgwProcessProgressChanged(self, sender, e):
        progress = e.ProgressPercentage
        self.SetProgress(progress, e.UserState)
        pass
    
    def SetProgress(self, progress, userState):
        if self.InvokeRequired:
            self.Invoke(self.SetProgress, [progress, userState])
            return

        count = userState[0]
        booklen = len(self.Books)
        max = self.TotalRulesets * booklen

        if count == 999999:
            self.countRuleset += 1
            progress = (self.countRuleset * 100.0) / max
        else:
            progress = ((self.TotalRulesets * count) * 100) / max

        self._progressBar1.Value = progress
        if isinstance(userState[1], str):
            self._textBox1.Text = userState[1]
        else:
            self._label2.Text = userState[1].CaptionWithoutTitle

        self._progressBar1.Value = progress
        if count != 999999 and count < booklen: self._label1.Text = 'Processing ' + (count + 1).ToString() + ' of ' + booklen.ToString() + ' books'
        pass

    def BtnCancelClick(self,sender, e):
        if self._bgwProcess.IsBusy:
            self._bgwProcess.CancelAsync()
        else:
            self.Close()

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