# some variables for global use
import clr
import System
from System.IO import Path, FileInfo
import iniReadWrite
from System import Array
from System import StringSplitOptions
from iniReadWrite import *
from System.Collections.Generic import Dictionary
#clr.AddReference("ComicRack.Engine")
from cYo.Projects.ComicRack.Engine import MangaYesNo, YesNo


############Set Paths##############
FOLDER = FileInfo(__file__).DirectoryName + Path.DirectorySeparatorChar.ToString()
IMGFOLDER = FOLDER
DATFILE = Path.Combine(FOLDER, 'dataMan.dat') #can load 1.24 text files or 2.3.1 xml files saves as xml
SAMPLEFILE = Path.Combine(FOLDER, 'dataManSample.dat')
INIFILE = Path.Combine(FOLDER, 'dataMan.ini')
USERINI = Path.Combine(FOLDER, 'user.ini')
BAKFILE = Path.Combine(FOLDER, 'dataMan.bak')
ERRFILE = Path.Combine(FOLDER, 'dataMan.err')
TMPFILE = Path.Combine(FOLDER, 'dataMan.tmp')
LOGFILE = Path.Combine(FOLDER, 'dataMan.log')
CHKFILE = Path.Combine(FOLDER, 'dataMan.chk')                # will be created once the configuration is saved
GUIEXE = Path.Combine(FOLDER, 'crdmgui.exe')

##############End Set Paths##############

################Set Constant variables##############

CRLISTDELIMITER_JOIN = ', '
CRLISTDELIMITER_SPLIT = ','

GROUPHEADER = '#@ GROUP '
RULESETHEADER = '#@ NAME '
GROUPENDER = '#@ END_GROUP'

ENDER = '#@ END_RULES'
AUTHORHEADER = '#@ AUTHOR'
NOTESHEADER = '#@ NOTES'

########################### Images #############################

ICON_SMALL = Path.Combine(IMGFOLDER, 'dataMan16.ico')
ICON = Path.Combine(IMGFOLDER, 'dataMan.ico')
IMAGE = Path.Combine(IMGFOLDER, 'dataMan.png')
IMAGESEARCH = Path.Combine(IMGFOLDER, 'search.png')
IMAGEADD = Path.Combine(IMGFOLDER, 'yes.png')
IMAGEAPPLY = Path.Combine(IMGFOLDER, 'Apply.png')
IMAGETRASH = Path.Combine(IMGFOLDER, 'Trash.png')
IMAGEDELETE_SMALL = Path.Combine(IMGFOLDER, 'erase.png')
IMAGEDOWN = Path.Combine(IMGFOLDER, 'down.png')
IMAGELIGHTNING = Path.Combine(IMGFOLDER, 'lightning.png')
IMAGETEXT = Path.Combine(IMGFOLDER, 'text.png')
DONATE = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UQ7JZY366R85S'
WIKI = 'http://code.google.com/p/cr-data-manager/'
MANUAL = 'http://code.google.com/p/cr-data-manager/downloads/list'

COMPARE_CASE_SENSITIVE = ReadKeyAsBool(USERINI, 'CaseSensitive')


#############End set constant variables##################

######################Read From dataman.ini###############################
VERSION = System.Version(ReadKey(INIFILE,'Version'))
DMLISTDELIMITER = ReadKey(INIFILE, 'ListDelimiter')
DATEFORMAT = ReadKey(INIFILE, 'DateTimeFormat')

####FIELDTYPES AND ALLOWED MODIFIERS#########
ALLOWEDKEYS = ReadKeyAsStringList(INIFILE, 'allowedKeys')
ALLOWEDVALS = ReadKeyAsStringList(INIFILE, 'allowedVals')
READONLYKEYS = ReadKeyAsStringList(INIFILE, 'ReadOnlyKeys')

ALLOWEDKEYMODIFIERS = ReadKeyAsStringList(INIFILE, 'allowedKeyModifiers')
ALLOWEDVALMODIFIERS = ReadKeyAsStringList(INIFILE, 'allowedValModifiers')

FIELDSSTRING = ReadKeyAsStringList(INIFILE, 'stringKeys')
ALLOWEDKEYMODIFIERSSTRING = ReadKeyAsStringList(INIFILE, 'allowedKeyModifiersString')
ALLOWEDVALMODIFIERSSTRING = ReadKeyAsStringList(INIFILE, 'allowedValModifiersString')

FIELDSLIST = ReadKeyAsStringList(INIFILE, 'multiValueKeys')
ALLOWEDKEYMODIFIERSLIST = ReadKeyAsStringList(INIFILE, 'allowedKeyModifiersMulti')
ALLOWEDVALMODIFIERSLIST = ReadKeyAsStringList(INIFILE, 'allowedValModifiersMulti')

FIELDSDATETIME = ReadKeyAsStringList(INIFILE, 'dateTimeKeys')
ALLOWEDKEYMODIFIERSDATETIME = ReadKeyAsStringList(INIFILE, 'allowedKeyModifierDateTime')
ALLOWEDVALMODIFIERSDATETIME = ReadKeyAsStringList(INIFILE, 'allowedValModifierDateTime')

FIELDSLANGUAGEISO = ReadKeyAsStringList(INIFILE, 'languageISOKeys')
ALLOWEDKEYMODIFIERSLANGUAGEISO = ReadKeyAsStringList(INIFILE, 'allowedKeyModifierLanguageISO')
ALLOWEDVALMODIFIERSLANGUAGEISO = ReadKeyAsStringList(INIFILE, 'allowedValModifierLanguageISO')

FIELDSMANGAYESNO = ReadKeyAsStringList(INIFILE, 'mangaYesNoKeys')
ALLOWEDKEYMODIFIERSMANGAYESNO = ReadKeyAsStringList(INIFILE, 'allowedKeyModifierMangaYesNo')
ALLOWEDVALMODIFIERSMANGAYESNO = ReadKeyAsStringList(INIFILE, 'allowedValModifierMangaYesNo')

FIELDSYESNO = ReadKeyAsStringList(INIFILE, 'yesNoKeys')
ALLOWEDKEYMODIFIERSYESNO = ReadKeyAsStringList(INIFILE, 'allowedKeyModifierYesNo')
ALLOWEDVALMODIFIERSYESNO = ReadKeyAsStringList(INIFILE, 'allowedValModifierYesNo')

FIELDSBOOL = ReadKeyAsStringList(INIFILE, 'boolKeys')
ALLOWEDKEYMODIFIERSBOOL = ReadKeyAsStringList(INIFILE, 'allowedKeyModifierBool')
ALLOWEDVALMODIFIERSBOOL = ReadKeyAsStringList(INIFILE, 'allowedValModifierBool')

ALLOWEDKEYMODIFIERSCUSTOM = ReadKeyAsStringList(INIFILE, 'allowedKeyModifierString')
ALLOWEDVALMODIFIERSCUSTOM = ReadKeyAsStringList(INIFILE, 'allowedValModifierString')

FIELDSNUMERIC = ReadKeyAsStringList(INIFILE, 'numericalKeys')
ALLOWEDKEYMODIFIERSNUMERIC = ReadKeyAsStringList(INIFILE, 'allowedKeyModifiersNumeric')
ALLOWEDVALMODIFIERSNUMERIC = ReadKeyAsStringList(INIFILE, 'allowedValModifiersNumeric')

FIELDSPSUEDONUMERIC = ReadKeyAsStringList(INIFILE, 'pseudoNumericalKeys')
ALLOWEDKEYMODIFIERSPSEUDONUMERIC = ReadKeyAsStringList(INIFILE, 'allowedKeyModifiersPseudoNumeric')
ALLOWEDVALMODIFIERSPSEUDONUMERIC = ReadKeyAsStringList(INIFILE, 'allowedValModifiersPseudoNumeric')

REGEXVARREPLACEKEYS = ReadKeyAsStringList(INIFILE, 'regExVarReplaceFields')

MULTIPARAMMODIFIERS = ReadKeyAsStringList(INIFILE, 'multipleParamModifiers')

FIELDSMULTILINE = ReadKeyAsStringList(INIFILE, 'multiLineKeys')
####END FIELDTYPES AND ALLOWED MODIFIERS#########
#################End read From dataman.ini############################

#####################Read From User.ini#######################
BreakAfterFirstError = ReadKeyAsBool(USERINI, "BreakAfterFirstError")
TraceGeneralMessages = ReadKeyAsBool(USERINI,  'TraceGeneralMessages')
TraceFunctionMessages = ReadKeyAsBool(USERINI,  'TraceFunctionMessages')
SortLists = ReadKeyAsBool(USERINI,  'SortLists')
#############type conversion utilities ########################

def StringToDate(strDate):
    if strDate == '':
        return System.DateTime(1,1,1)    
    return System.DateTime.Parse(strDate)

def IsDateTime(value):
    return isinstance(value, System.DateTime)

def StringToInt(strNumber):
    if strNumber == '':
            return int(-1)
    return int(strNumber)

def IsInt(value):
    return isinstance(value, System.Int32)

def StringToFloat(strFloat):
    fValue = float(-1)
    fValue = float(strFloat)    
    return fValue    

def IsFloat(value):
    return isinstance(value, float)

def CRStringToList(strList):
        return (x.strip for x in strList.Split(Array[str](CRLISTDELIMITER_SPLIT), StringSplitOptions.RemoveEmptyEntries))

def ListTOCRString(list):
    return CRLISTDELIMITER_JOIN.join([unicode(x) for x in list])

def DMStringToList(strList):
        return strList.split(DMLISTDELIMITER)

def IsList(value):
    return isinstance(value, list) or isinstance(value, Array[str])

#all of the below will throw errors if the conversion is not possible
#this behaviour is intended and should be caught in the calling function
#which should report errors at runtime or in the log

def StringToBool(strValue):
    return bool.Parse(strValue)

def IsBool(value):
    return isinstance(value, bool)

def IsYesNo(value):
    return isinstance(value, YesNo)		
	
def StringToYesNo(strValue):
    ynReturn = None
    if strValue == 'Unknown' or strValue == '':
        ynReturn = YesNo.Unknown
    elif strValue.lower() == 'yes':
        ynReturn = YesNo.Yes
    elif strValue.lower() == 'no':
        ynReturn = YesNo.No

    if ynReturn == None:
        raise dmConversionError(strValue, 'ComicRack.Engine.YesNo')
    return ynReturn

def YesNoToString(YesNoValue):
    strReturn = ''
    if MangaYesNoValue == YesNo.Yes:
        strReturn = 'Yes'
    elif MangaYesNoValue == YesNo.No:
        strReturn = 'No'

    return strReturn

def IsMangaYesNo(value):
    return isinstance(value, MangaYesNo)
	
def StringToMangaYesNo(strValue):
    ynReturn = None
    if strValue.lower() == 'yes':
        ynReturn = MangaYesNo.Yes
    elif strValue.lower() == 'no':
        ynReturn = MangaYesNo.No
    elif strValue.lower() == 'yesandrighttoleft':
        ynReturn = MangaYesNo.YesAndRightToLeft
    else:
        ynReturn = MangaYesNo.Unknown		 							 

    if ynReturn == None:
        raise dmConversionError(strValue, 'ComicRack.Engine.MangaYesNo')
    
    return ynReturn

def ToString(obj):
    strReturn = ''
    if isinstance(obj, YesNo):
        if obj == YesNo.Unknown:
            strReturn = ''
        else:
            strReturn = obj.ToString()
    elif isinstance(obj, MangaYesNo):
        if obj == MangaYesNo.Unknown:
            strReturn = ''
        else:
            strReturn = obj.ToString()
        pass
    elif isinstance(obj, System.DateTime):
        strReturn = obj.ToString(DATEFORMAT)
    elif IsList(obj):
        strReturn = ListTOCRString(obj)
    else:
        strReturn = obj.ToString()

    return strReturn

#############end conversion utilities###############

#######Field And Modifier helpers##############
def ValidModifiers(strKey, strRuleOrAction):
        strListReturn = []
        if strRuleOrAction.lower() == 'rule':
                strListReturn = ValidKeyModifiers(strKey)
        elif strRuleOrAction.lower() == 'action':
                strListReturn = ValidValModifiers(strKey)
        return strListReturn

def ValidKeyModifiers(strKey):
        strListReturn = []
        if KeyFieldType(strKey) == 'STRING':
                strListReturn = ALLOWEDKEYMODIFIERSSTRING
        elif KeyFieldType(strKey) == 'LIST':
                strListReturn = ALLOWEDKEYMODIFIERSLIST
        elif KeyFieldType(strKey) == 'DATETIME':
                strListReturn = ALLOWEDKEYMODIFIERSDATETIME
        elif KeyFieldType(strKey) == 'BOOL':
                strListReturn = ALLOWEDKEYMODIFIERSBOOL
        elif KeyFieldType(strKey) == 'YESNO':
                strListReturn = ALLOWEDKEYMODIFIERSYESNO
        elif KeyFieldType(strKey) == 'NUMERIC':
                strListReturn = ALLOWEDKEYMODIFIERSNUMERIC
        elif KeyFieldType(strKey) == 'PSUEDONUMERIC':
                strListReturn = ALLOWEDKEYMODIFIERSPSEUDONUMERIC
        elif KeyFieldType(strKey) == 'LANGUAGEISO':
                strListReturn = ALLOWEDKEYMODIFIERSLANGUAGEISO
        return strListReturn

def ValidValModifiers(strKey):
        strListReturn = []
        if KeyFieldType(strKey) == 'STRING':
                strListReturn = ALLOWEDVALMODIFIERSSTRING
        elif KeyFieldType(strKey) == 'LIST':
                strListReturn = ALLOWEDVALMODIFIERSLIST
        elif KeyFieldType(strKey) == 'DATETIME':
                strListReturn = ALLOWEDVALMODIFIERSDATETIME
        elif KeyFieldType(strKey) == 'BOOL':
                strListReturn = ALLOWEDVALMODIFIERSBOOL
        elif KeyFieldType(strKey) == 'YESNO':
                strListReturn = ALLOWEDVALMODIFIERSYESNO
        elif KeyFieldType(strKey) == 'NUMERIC':
                strListReturn = ALLOWEDVALMODIFIERSNUMERIC
        elif KeyFieldType(strKey) == 'PSUEDONUMERIC':
                strListReturn = ALLOWEDVALMODIFIERSPSEUDONUMERIC
        elif KeyFieldType(strKey) == 'LANGUAGEISO':
                strListReturn = ALLOWEDVALMODIFIERSLANGUAGEISO        
        if strKey in REGEXVARREPLACEKEYS:
                strListReturn.append('RegExVarReplace')
                strListReturn.append('RegExVarAppend')
        return strListReturn

def KeyFieldType(strKey):
        strReturn = 'UNKNOWN'
        
        if strKey in FIELDSSTRING:
                strReturn = 'STRING'
        elif strKey in FIELDSLIST:
                strReturn = 'LIST'
        elif strKey in FIELDSDATETIME:
                strReturn = 'DATETIME'
        elif strKey in FIELDSBOOL:
                strReturn = 'BOOL'
        elif strKey in FIELDSYESNO:
                strReturn = 'YESNO'
        elif strKey in FIELDSMANGAYESNO:
                strReturn = 'MANGAYESNO'
        elif strKey in FILEDSNUMERIC:
                strReturn = 'NUMERIC'
        elif strKey in FIELDSPSUEDONUMERIC:
                strReturn = 'PSUEDONUMERIC'
        elif strKey in FIELDSLANGUAGEISO:
                strReturn = 'LANGUAGEISO'
        return strReturn

def GetAvailableKeys(strRuleOrAction):
        strListReturn = []
        if strRuleOrAction.lower() == 'rule':
                strListReturn.extend(ALLOWEDKEYS)
        elif strRuleOrAction == 'action':
                strListReturn.extend(ALLOWEDVALS)
                strListReturn.extend(REGEXVARREPLACEKEYS)
        return strListReturn

def GetAppendString(strKey):
        if strKey in FIELDSMULTILINE:
                return "\r\n"
        else:
           return ", "

        pass

def GetValueType(strFieldName):
    strReturn = unknown
    #String
    if strFieldName in FIELDSSTRING or strFieldName in FIELDSCUSTOM:
        strReturn = 'string'
    elif strFieldName in FIELDSNUMERIC:
        strReturn = 'numeric'
    elif strFieldName in FIELDSDATETIME:
        strReturn = 'datetime'
    elif strFieldName in FIELDSPSUEDONUMERIC:
        strReturn = 'psuedonumeric'
    elif strFieldName in FIELDSBOOL:
        strReturn = 'bool'
    elif strFieldName in FIELDSLIST:
        strReturn = 'list'
    elif strFieldName in FILEDSLANGUAGEISO:
        strReturn = 'languageiso'
    elif strFieldName in FIELDSYESNO:
        strReturn = 'yesno'
    elif strFieldName in FIELDSMANGAYESNO:
        strReturn = 'mangayesno'
    return strReturn

def ComicVineFields():
        return ['Series','Volume','Number','Title','Published','ReleasedTime','AlternateSeries','Publisher','Imprint','Writer','Penciller','Colorist','Inker','Letterer','CoverArtist','Editor','Summary','Characters']

#######Field And Modifier helpers##############

def WriteStartTime():
    WriteKey(USERINI, 'LastProcessStart', System.DateTime.Now.ToString('yyyy/MM/dd hh:mm:ss'))

def WriteEndTime():
    WriteKey(USERINI, 'LastProcessEnd', System.DateTime.Now.ToString('yyyy/MM/dd hh:mm:ss'))

def WriteDurationtime(strDuration):
    WriteKey(USERINI, 'LastProcessDuration', strDuration)

#################### Book Helpers #####################
def CompareValues(book, cmpDict):
    """Compares Values of book to a dictionary of values to see if any values have changed
    
        Attributes:
            book -- the comicbook object holding current values after process has run
            cmpDict -- The Dictionary of values that before the process
            
    
    """
    strReturn = ''

    touchedFields = 0
    
    for field in cmpDict:
        bookValue = None
        if field in ALLOWEDVALS:
            bookValue = getattr(book, field)
        else:
            try:
                bookValue = book.GetCustomValue(field)
            except Exception as er:
                bookValue = ''


        if  bookValue != cmpDict[field]:
            touchedFields = touchedFields + 1
            
            extrastring = ''
            if not field in ALLOWEDVALS:
                extrastring = 'Custom '

            strReturn = strReturn + '    ' + extrastring + 'Field: ' + field
            strReturn = strReturn + '        Previous Value: ' + cmpDict[field] + System.Environment.NewLine
            strReturn = strReturn + '        New Value: ' + bookValue.ToString() + System.Environment.NewLine
    return strReturn

def CreateBookDict(book):
    dictReturn = dict()
    for item in ALLOWEDVALS:
        if item != 'Custom':
            dictReturn[item] = getattr(book, item)
        else:
            customs = book.GetCustomValues()
            for field in customs:
                dictReturn[field.Key] = field.Value
            pass
        pass
    return dictReturn

def AppendReport(strInitialReport, strExtendReport):
    strReturn = ''
    if strInitialReport == None or strInitialReport == '':
        strReturn = strExtendReport
    else:
        strReturn = strInitialReport + System.Environment.NewLine + strExtendReport 
    return strReturn

def GetTouchCount(book, tmpDict):
    touchedFields = 0
    
    for field in tmpDict:
        bookValue = None
        if field in ALLOWEDVALS:
            bookValue = getattr(book, field)
        else:
            try:
                bookValue = book.GetCustomValue(field)
            except Exception as er:
                bookValue = ''


        if  bookValue != tmpDict[field]:
            touchedFields = touchedFields + 1
            
    return touchedFields

def IsCustomField(strFieldName):
    bCustom = True



    return bCustom

################ Errors ################

class dmException(Exception):
    @property
    def Message(self):
        return self.msg

    def __init__(self, strMessage):
        self.msg = strMessage

class dmConversionError(dmException):    
    
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.msg = 'Could not convert \'' + self.value + '\' to type \'' + self.type + '\'.'
        pass

def GetStringAsList(strList):
    return (x.strip for x in strList.Split(CRLISTDELIMITER_SPLIT))

class dmNodeCompileException(dmException):
    def __init__(self, strMessage, dmNodeParent):
        dmException.__init__(self, strMessage)
        self.Parent = dmNodeParent

class dmGroupCompileException(dmNodeCompileException):
    def __init__(strMessage, dmContainerParent):
        dmNodeCompileException.__init__(self, strMessage ,dmNodeParent)

class dmCollectionCompileError(dmNodeCompileException):
    def __init__(self, strMessage, dmNodeParent):
        dmNodeCompileException.__init__(self, strMessage, dmNodeParent)