import clr
import sys
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')


import System.Drawing
import System.Windows.Forms
import System.Diagnostics
import dmClasses
import dmGlobals
import iniReadWrite
import runProcess

from dmClasses import *
from System.Diagnostics import Process
from runProcess import runProcess
from frmProfile import frmProfile
# this handles unicode encoding:
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

def crVersion():
	''' checks the CR version if it is min. 0.9.164 (for custom values) '''
	minVersion = '0.9.164'		# we need CR 0.9.164 minimum (for custom values)
	vMin = 0 + 9000 + 164
	myVersion = ComicRack.App.ProductVersion	# get the installed CR version number
	v = myVersion.split('.')
	vMyVersion = (int(v[0]) * 1000000) + (int(v[1]) * 1000) + int(v[2])
	if vMyVersion < vMin:		# if actual version is lower than minimum version: return False
		MessageBox.Show(
		'You have only CR version %s installed.\nPlease install at least version %s of ComicRack first!' % (myVersion,minVersion),
		'Data Manger for ComicRack %s' % globalvars.VERSION)
		return False
	return True

# ============================================================================      
# hook to run the configScript
#@Name	 Data Manager configuration
#@Key    data-manager-mod
#@Hook   ConfigScript
# ============================================================================
def dmRunConfig():
    #read ini info
    p = System.Diagnostics.Process()
    p.StartInfo.FileName = dmGlobals.GUIEXE
    p.Start()
    pass


# ============================================================================ 
# hook to run the main dataManager loop
#@Name	Data Manager Mod
#@Image dataMan16.png
#@Key	data-manager-mod
#@Hook	Books
# ============================================================================
def dmRunProcess(books):
	form = frmProfile(dmGlobals.FOLDER)
	form.ShowDialog(ComicRack.MainWindow)
	if File.Exists(form.ChosenProfile):
		if len(books) > 0:
			collection = dmCollection(form.ChosenProfile)
			processor = runProcess(books,collection)
			processor.ShowDialog(ComicRack.MainWindow)
			processor.Dispose()
			pass
	elif File.Exists(dmGlobals.OLDDATFILE):
		pass
	else:
		System.Windows.Forms.MessageBox.Show("There is no Ruleset Collection to process.\r\nPlease use configuration to set up your rules", "No Ruleset Defined", System.Windows.Forms.MessageBoxButtons.OK)
	
	form.Dispose()
	pass

def dmAutoCreateRules(books):
	if not File.Exists(dmGlobals.AUTOCREATEFILE):
		if System.Windows.Forms.MessageBox.Show('No Auto create Rule definitions exist\r\nWould you like to manage them now?', 'No definitions exist', System.Windows.Forms.MessageBoxButtons.YesNo) == System.Windows.Forms.DialogResult.Yes:
			dmConfigAutocreateRun(books)
		else:
			pass
	else:
		dmAutoCreateQuickDialog(books)
	pass

def dmAutoCreateQuickDialog(books):
	if books != None:
		
		pass
	pass


def dmConfigAutoCreate():
	books = ComicRack.App.GetLibraryBooks()			
	pass

def dmConfigAutocreateRun(books):

    pass