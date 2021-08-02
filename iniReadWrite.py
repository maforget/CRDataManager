import clr
import System
import System.IO

from System.IO import File, Path, Directory

def ReadKey(iniFilePath, strKey):
    dictKeys = LoadFile(iniFilePath)
    strReturn = ''
    if dictKeys.has_key(strKey):
        strReturn = dictKeys[strKey]
    return strReturn

def ReadKeyAsStringList(iniFilePath, strKey):
    dictKeys = LoadFile(iniFilePath)
    ListReturn = []
    if  dictKeys.has_key(strKey):
        ListReturn = dictKeys[strKey].split(',')
    return ListReturn

def ReadKeyAsBool(iniFilePath, strKey):
    dictKeys = LoadFile(iniFilePath)
    bReturn = False
    try:
        bReturn = bool.Parse(dictKeys[strKey])
    except:
        pass
    return bReturn

def WriteKey(iniFilePath, strKey, strValue):
    dictKeys = LoadFile(iniFilePath)
    dictKeys[strKey] = strValue
    strFile = ""
    for item in dictKeys:
        strFile += item + ' = ' + dictKeys[item] + System.Environment.NewLine
    File.WriteAllText(iniFilePath, strFile)
    pass

def LoadFile(iniFilePath):
    dictKeys = dict()
    if File.Exists(iniFilePath):
        KeyLines = File.ReadAllLines(iniFilePath)
        for line in KeyLines:
            if not line.startswith(';') and not line.strip() == '':
                dictKeys.Add(line.split(' = ')[0].strip(),line.split('=')[1].strip())
    return dictKeys