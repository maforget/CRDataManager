import clr
import System
import System.IO
import dmGlobals
from __builtin__ import isinstance
from System import StringSplitOptions
from System import Array

clr.AddReference('System.Text.RegularExpressions')
clr.AddReference('System.Xml.Linq')

import System.Text.RegularExpressions
import System.Xml

from dmGlobals import dmConversionError

from System.Text.RegularExpressions import Regex, RegexOptions, Match
from System.Collections.Generic import List
from System.Xml.Linq import *
from System.Collections.Generic import Dictionary, List

from dmGlobals import *
from System.IO import File, Directory

class dmNode:
    """Base of all classes used in a dmCollection"""

    def getName(self): return self.__Name
    def setName(self, strName): self.__Name = strName
    Name = property(getName, setName)

    def getComment(self): return self.__Comment
    def setComment(self, strComment): self.__Comment = strComment
    Comment = property(getComment, setComment)

    def getParent(self): return self.__Parent
    def setParent(self, dmcContainer): return self.__Parent
    Parent = property(getParent, setParent)

    def __init__(self, dmnparent, strParameters):
        if dmGlobals.TraceFunctionMessages:
            print 'dmNode constructor: dmNode(dmNodeParent, strParameters)'

        self.Parent = dmnparent #this is not necessary for processing dmNodes while running but will come in handy for the editor
        self.Name = '' #all inheriting nodes are capable of having a name
        self.Comment = '' #all inheriting nodes are capabale of having a comment
        
        pass

    def ToXML(self, elementName):
        if dmGlobals.TraceFunctionMessages:
            print 'Method dmNode:ToXML(elementName)'

        baseElement = XElement(XName.Get(elementName))
        
        if self.Name != '' and self.Name != None: 
            baseElement.Add(Xattribute(XName.Get('name'), self.Name))
            
        if self.Comment != '' and self.Comment != None:
            baseElement.Add(XAttribute(XName.Get('comment'), self.Comment))
            
        return baseElement

    def FromXML(self, element):
        if dmGlobals.TraceFunctionMessages:
            print 'Method dmNode:ToXML(element)'

        if element.Attribute(XName.Get('name')) != None:
           self.Name = element.Attribute(XName.Get('name')).Value
           
        if element.Attribute(XName.Get('comment')) != None:
           self.Comment = element.Attribute(('comment')).Value
           
        pass

    def ProcessBook(self, book, bgWorker):
        if dmGlobals.TraceFunctionMessages:
            print 'Method: dmNode:ProcessBook(book, backgroundWorker)'

        strReport = ''
        
        return strReport

class dmContainer(dmNode):
    """a container that contains groups and rulesets [base for dmCollection and dmGroup]"""

    def getGroups(self): return self.__Groups
    def setGroups(self, groups): self.__Groups = List[dmGroup](groups)
    Groups = property(getGroups, setGroups)

    def getRulesets(self): return self.__Rulesets
    def setRulesets(self, rulesets): self.__Rulesets = List[dmRuleset](rulesets)
    Rulesets = property(getRulesets, setRulesets)

    def __init__(self, dmnparent, strParameters):
        """Initializes a dmContainer object"""
        if dmGlobals.TraceFunctionMessages:
            print 'dmContainer constructor: dmContainer(dmNodeParent, objParameters)'

        dmNode.__init__(self, dmnparent, strParameters) #initialize all properties inheirited from dmNode
        
        self.Groups = [] #create Group List
        self.Rulesets = [] #create Ruleset List        

        pass

    def ParseGroup(self, arrParameters, nStartLine, dmcParent):
        if dmGlobals.TraceFunctionMessages:
            print 'Method dmConainer:ParseGroup(stingarrayParameters, intStartLine, dmContainerToAddTo)'

        nReturn = nStartLine #integer value that will send back the line number of the final line parsed
        newGroup = dmGroup(dmcParent, None) #create a new group that will hold the new group info

        #Parse Group Info from line
        if arrParameters[nReturn].startswith(GROUPHEADER): #if the current line starts with the defined GROUP HEADER in dmGlobals
            GroupInfo = self.ParseNodeInfo(arrParameters[nReturn]) #Parse info for new Group into a dict Item
            
            newGroup.Name = GroupInfo['GROUP'].strip() #set Group name from group info
            
            if GroupInfo.has_key('COMMENT'): #if Comment is provided in GroupInfo
                newGroup.Comment = GroupInfo['COMMENT'].strip() #set Comment from GroupInfo
                
            if GroupInfo.has_key('FILTERSANDDEFAULTS'): #if FILTERSANDDEFAULTS exixts in Group Info
                newGroup.FiltersAndDefaults = dmRuleset(None, GroupInfo['FILTERSANDDEFAULTS'].strip()) #set the FiltersAndDefaults Ruleset
                
            nReturn = nReturn + 1 #increment current line number

        while not arrParameters[nReturn].startswith(dmGlobals.GROUPENDER): #if the line does not equal the "GROUPENDER" defined in dmGlobals
            if arrParameters[nReturn].startswith(dmGlobals.GROUPHEADER): #If CURRENT line is a group header
                nReturn = self.ParseGroup(arrParameters, nReturn, newGroup) #create and a new Group with this group as parent
            elif arrParameters[nReturn].startswith(dmGlobals.RULESETHEADER) or not arrParameters[nReturn].startswith('#'): #else if the current line is a RULESETHEADER or uncommented line
                nReturn = self.ParseRuleset(arrParameters, nReturn, newGroup)  #Parse and add new Ruleset to this group
            else: #otherwise
                nReturn = nReturn + 1 #increment line number

        
        dmcParent.Groups.Add(newGroup) #finally add the created group to the dmContainer node defined as dmcParent
        
        nReturn = nReturn + 1 #increment line number

        return nReturn #return next

    def ParseRuleset(self, arrParameters, nStartLine, dmcParent):
        """Parses Ruleset as a child Ruleset of the dmContainer: dmcParent"""
        if dmGlobals.TraceFunctionMessages:
            print 'Method: dmContainer:ParseRuleset(stringarrayParameters, intStartLine, dmContainerToMakeParent)'

        nReturn = nStartLine #assign current defined start line as the line number to return

        newRuleset = dmRuleset(dmcParent, None) #create a new Ruleset to house parsed info
        
        if arrParameters[nReturn].startswith(dmGlobals.RULESETHEADER): #if the current line is a RulesetHeader
            RulesetInfo = self.ParseNodeInfo(arrParameters[nReturn]) #Parse Ruleset Info from line
            
            if RulesetInfo.has_key('NAME'): #if Ruleset Info Contains a Name key
                newRuleset.Name = RulesetInfo['NAME'] #set new Ruleset Name
                
            if RulesetInfo.has_key('COMMENT'): #if Ruleset Info Contains a Comment Key
                newRuleset.Comment = RulesetInfo['COMMENT'] #set new Ruleset Comment
                
            nReturn = nReturn + 1 #after parsing Ruleset Info move to next line
        
        newRuleset.ParseParameters(arrParameters[nReturn]) #actually parse ruleset if line is ruleset
        
        nReturn = nReturn + 1 #set Next Line as the return value
                
        dmcParent.Rulesets.Add(newRuleset) # add new Ruleset to dmContainer dmcParent
        
        return nReturn #return next line value

    def ParseNodeInfo(self, strInfo):
        """Retrieves info values from headers"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmContainer:ParseNodeInfo(stringInfo)'
        NodeInfo = dict() #setup a dictionary to hold values

        parseInfo = strInfo.strip('#') #strip Comment item
        parseInfo = parseInfo.lstrip('@ ')
        listInfo = parseInfo.split('@ ') #use @ to split Values

        for item in listInfo:
            if item != None and item.strip() != '':
                dicItem = item.strip().split(' ',1)
                if len(dicItem) > 1:
                    NodeInfo[dicItem[0]] = dicItem[1]
                elif len(dicItem) > 0:
                    NodeInfo[dicItem[0]] = ''
        return NodeInfo

    def ParseParameters(self, strParameters):
        """does nothing, define this in inherited dmContainers"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmContainer:ParseParameters(objParameters)'
        pass

    def ProcessBook(self, book, bgWorker):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmContainer:ProcessBook(book, backgroundWorker)'
        strReport = ''

        if not bgWorker.CancellationPending:
            if dmGlobals.TraceGeneralMessages: print "Processing child groups..."
            for group in self.Groups:
                if dmGlobals.TraceGeneralMessages: print 'verifying user has not cancelled process...'
                if not bgWorker.CancellationPending:
                    strGroupReport = group.ProcessBook(book, bgWorker)
                    if strGroupReport != None and strGroupReport != '':
                        strReport = dmGlobals.AppendReport(strReport, strGroupReport)
                else:
                    strReport = strReport + System.Environment.NewLine + 'Process cancelled by user'
                    if dmGlobals.TraceGeneralMessages: 
                        print 'Process cancelled by user'
                        print 'backing out of process...'
                    break
            if dmGlobals.TraceGeneralMessages: print "Processing child rulesets..."
            for ruleset in self.Rulesets:
                if dmGlobals.TraceGeneralMessages: print 'verifying user has not cancelled process...'
                if not bgWorker.CancellationPending:
                    if dmGlobals.TraceGeneralMessages: print 'Processing book...'
                    strRulesetReport = ruleset.ProcessBook(book, bgWorker)
                    bgWorker.ReportProgress(0, [999999, book])
                    if strRulesetReport != None and strRulesetReport != '':
                        strReport = dmGlobals.AppendReport(strReport, strRulesetReport)
                else:
                    if dmGlobals.TraceGeneralMessages: 
                        print 'Process cancelled by user'
                        print 'backing out of process...'
                    break
        else:
            strReport = dmGlobals.AppendReport(strReport, System.Environment.NewLine + 'Process cancelled by user')
            if dmGlobals.TraceGeneralMessages: 
                print 'Process cancelled by user'
                print 'backing out of process...'
        if dmGlobals.TraceFunctionMessages: print 'Exiting process dmContainer:ProcessBook(book, bgWorker)'
        return strReport

    def ToXML(self, elementName):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmContainer:ToXML(stringElementName)'
        baseElement = dmNode.ToXML(self, elementName)
        for item in self.Groups:
            baseElement.append(item.XMLSerialize('group'))
        for item in self.Rulesets:
            baseElement.append(item.XMLSerialize('ruleset'))
        return baseElement

    def FromXML(self, element):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmContainer:FromXML(xmlElement)'
        dmNode.FromXML(self, element)
        
        for group in element.Elements(XName.Get('group')):
            self.Groups.append(dmGroup(self, group))
        for ruleset in element.Elements(XName.Get('ruleset')):
            self.Rulesets.append(dmRuleset(self, ruleset))
        pass

class dmCollection(dmContainer):
    """The base object for groups and rulesets"""
    
    def getDisabled(self): return self.__Disabled
    def setDisabled(self, dmgGroup): self.__Disabled = dmgGroup
    Disabled = property(getDisabled, setDisabled)
    
    def getVersion(self): return self.__Version
    def setVersion(self, version): self.__setversion__(version)
    Version = property(getVersion, setVersion)

    def __init__(self, strParameters):
        if dmGlobals.TraceFunctionMessages: print 'dmCollection constructor: dmCollection(objParameters)'
        if dmGlobals.TraceGeneralMessages: print 'Compiling Ruleset Collection'
        dmContainer.__init__(self, None, strParameters)
        self.Disabled = dmGroup(self)
        self.Version = System.Version(1,1,9,9)
               
        if strParameters != None:
            if isinstance(strParameters, XElement):
                self.FromXML(strParameters)
            else:
                self.ParseParameters(strParameters)
        pass

    def __setversion__(self, vItem):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmCollection:__setversion__(objVersion)'
        if isinstance(vItem, System.Version):
            self.Version = vItem
        elif isinstance(vItem, str):
            self.Version = System.Version.Parse(vItem)

    def ParseParameters(self, strParameters):
        """Parses the file to a collection"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmCollection:ParseParameters(objParameters)'
        if File.Exists(strParameters):
            try:
                self.FromXML(System.Xml.Linq.XDocument.Load(strParameters).Root)
            except:
                self.Parse(File.ReadAllLines(strParameters))
        pass
    
    def Parse(self, arrParameters):
        """Parses the array of strings to a ruleset collection"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmCollection:Parse(stringarrayParameters)'
        nReturn = 0
        while nReturn < arrParameters.Length and not arrParameters[nReturn].startswith(dmGlobals.ENDER):
            if arrParameters[nReturn].startswith(dmGlobals.AUTHORHEADER):
                self.Name = arrParameters[nReturn].replace(dmGlobals.AUTHORHEADER,'')
                nReturn = nReturn + 1
            elif arrParameters[nReturn].startswith(dmGlobals.NOTESHEADER):
                nReturn = self.RetrieveNotes(arrParameters, nReturn)
            elif arrParameters[nReturn].startswith(dmGlobals.RULESETHEADER) or not arrParameters[nReturn].startswith('#'):
                nReturn = self.ParseRuleset(arrParameters, nReturn, self)
            elif arrParameters[nReturn].startswith(dmGlobals.GROUPHEADER):
                nReturn = self.ParseGroup(arrParameters, nReturn, self)
            else: nReturn = nReturn + 1
        pass

    def RetrieveNotes(self, arrParameters, nStartLine):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmCollection:RetrieveNotes(stringarrayParameters, intStartLine)'
        nReturn = nStartLine
        self.Comment = ''
        while not arrParameters[nReturn].startswith(NOTESENDER):
            self.Comment += arrParameters[nReturn].lstrip('# ') + System.Environment.NewLine
            nReturn = nReturn + 1
        pass

    def ProcessBook(self, book, bgWorker):
        if dmGlobals.TraceFunctionMessages:
            print 'Method: dmCollection:ProcessBook(book, backgroundWorker)'

        strReport = ''
        
        if not bgWorker.CancellationPending:
            strReport = dmContainer.ProcessBook(self, book, bgWorker)
            
        if dmGlobals.TraceFunctionMessages:
            print 'Exiting Method: dmCollection:ProcessBook(book, backgroundWorker)'

        return strReport
        
    def ToXML(self, elementName):
        if dmGlobals.TraceFunctionMessages:
            print 'Method: dmCollection:ToXML(stringElementName)'

        baseElement = dmContainer.ToXML(self, elementName)
        
        baseElement.Add(self.Disabled.XMLSerialize('disabled'))
        
        return baseElement

    def FromXML(self, element):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmCollection:FromXML(xmlElement)'
        dmContainer.FromXML(self, element)
        self.Disabled = dmGroup(self, element.Element(XName.Get('Disabled')))
        self.__setversion__(element.Attribute(XName.Get('version')).Value)
        pass
    
class dmGroup(dmContainer):
    """a named group of groups and rulesets (derived from dmContainer)"""

    def getFiltersAndDefaults(self): return self.__FiltersAndDefaults
    def setFiltersAndDefaults(self, dmrRuleset): self.__FiltersAndDefaults = dmrRuleset
    FiltersAndDefaults = property(getFiltersAndDefaults, setFiltersAndDefaults)

    def __init__(self, dmcparent, strParameters=None):
        if dmGlobals.TraceFunctionMessages: print 'dmGroup constructor: dmGroup(dmContainerParent, objParameters)'
        dmContainer.__init__(self, dmcparent, strParameters)
        self.FiltersAndDefaults = dmRuleset(self, None)
        
        if strParameters != None:
            if isinstance(strParameters, XElement):
                self.FromXML(strParameters)
            else:
                self.ParseParameters(strParameters)
        pass
    
    def ParseParameters(self, strParameters):
        """Parses Parameters of Group from a string or list of parameters"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmGroup:ParseParameters(objParameters)'
        if isinstance(strParameters, str) or isinstance(strParameters, list):
            arrParameters = list()
            if isinstance(strParameters, str):
                arrParameters = strParameters.splitlines() #split string into lines
            elif isinstance(strParameters, list):
                arrParameters = strParameters

            nReturn = 0
            #Parse Group Info from line
            if arrParameters[nReturn].startswith(GROUPHEADER):
                GroupInfo = self.ParseNodeInfo(arrParameters[nReturn])
                self.Name = GroupInfo['GROUP'].strip()
                if GroupInfo.haskey('COMMENT'):
                    self.Comment = GroupInfo['COMMENT'].strip()
                if GroupInfo.haskey('FILTERSANDDEFAULTS'):
                    self.FiltersAndDefaults = dmRuleset(self,GroupInfo['FILTERSANDDEFAULTS'].strip())
                #increment nReturn
                nReturn = nReturn + 1
    
            while nReturn < len(arrParameters) and not arrParameters[nReturn].startswith(GROUPENDER):
                if arrParameters[nReturn].startswith(GROUPHEADER):
                    nReturn = self.ParseGroup(arrParameters, nReturn, self)
                elif arrParameters[nReturn].startswith(RULESETHEADER) or not arrParameters[nReturn].startswith('#'):
                    nReturn = ParseRuleset(arrParameters, nReturn, self)
        elif isinstance(strParameters, XElement):
            self.FromXML(strParameters)
        pass
    
    def MeetsConditions(self, book):
        """Determines if the book matches all Rules in FiltersAndDefaults Ruleset"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmGroup:MeetsConditions(book)'
        return self.FiltersAndDefaults.MeetsConditions(book)

    def ProcessBook(self, book, bgWorker):
        if dmGlobals.TraceFunctionMessages:
            print 'Method: dmGroup:ProcessBook(book, backgroundWorker)'

        strReport = ''

        if self.MeetsConditions(book):
            if dmGlobals.TraceGeneralMessages: print 'Book: \'' + book.CaptionWithoutTitle + '\' Meets conditions, Processing.'
            strReport = dmContainer.ProcessBook(self, book, bgWorker)
            
            #groupReport
            CompiledReport = ''
            if dmGlobals.TraceGeneralMessages: print 'Applying Default actions of group \'' + self.Name
            
            strTempReport = ''
            for action in self.FiltersAndDefaults.Actions:
                strTempReport = action.Apply(book) + System.Environment.NewLine
                if strTempReport != None and strTempReport != '':
                    CompiledReport = CompiledReport + strTempReport
            if CompiledReport != '':
                CompiledReport = 'Group: \'' + self.Name + '\' touched book: ' + book.CaptionWithoutTitle + System.Environment.NewLine + CompiledReport
                strReport = strReport + System.Environment.NewLine + CompiledReport
        else:
            if dmGlobals.TraceGeneralMessages: print 'Conditions set forth by filters of group\'' + self.Name + '\' not met, skiping group.'
        
        if dmGlobals.TraceFunctionMessages: print 'Exiting Method: dmGroup:ProcessBook(book, backgroundWorker)'
        
        return strReport

    def ToXML(self, elementName):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmGroup:ToXML(stringElementName)'
        baseElement = dmContainer.ToXML(self, elementName)
        baseElement.Add(self.FiltersAndDefaults.ToXML('filtersanddefaults'))
        return baseElement

    def FromXML(self, element):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmGroup:FromXML(xmlElement)'
        dmContainer.FromXML(self, element)
        self.FiltersAndDefaults = dmRuleset(self, element.Element(XName.Get('filtersanddefaults')))
        pass

    def ToString(self):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmGroup:ToString()'
        strReturn = 'Group: ' + self.Name + ' ' + self.FiltersAndDefaults.HumanizeRules()
        return strReturn
    
class dmRuleset(dmNode):
    """Container for rules and actions"""

    def getRulesetMode(self): return self.__RulesetMode
    def setRulesetMode(self, strANDorOR): 
        if strANDorOR.lower() == 'and': self.__RulesetMode = 'AND'
        elif strANDorOR.lower() == 'or': self.__RulesetMode = 'OR'            
        else: self.__RulesetMode = 'AND'
    RulesetMode = property(getRulesetMode, setRulesetMode)

    def getRules(self): return self.__Rules
    def setRules(self, lstRules): self.__Rules = List[dmRule](lstRules)
    Rules = property(getRules, setRules)

    def getActions(self): return self.__Actions
    def setActions(self, lstActions): self.__Actions = List[dmAction](lstActions)
    Actions = property(getActions, setActions)

    def __init__(self, dmcparent, strParameters=None):
        """initializes ruleset instance"""
        if dmGlobals.TraceFunctionMessages: print 'dmRuleset constructor: dmRuleset(objParameters)'
        dmNode.__init__(self, dmcparent, strParameters) #calls base initialize which adds base fields
        self.RulesetMode = 'AND' #sets ruleset mode by default to AND ParseParameters call (from dmNode) later corrrects if and is used
        self.Rules = [] #initializes list of rules
        self.Actions = [] #initializes list of actions
        
        if strParameters != None:
            if isinstance(strParameters, XElement):
                self.FromXML(strParameters)
            else:
                self.ParseParameters(strParameters)
        pass

    def ParseParameters(self, strParameters):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:ParseParameters(objParameters)'
        if isinstance(strParameters, str):
            strParsed = strParameters
            """parses ruleset""" #note: this function is called from dmNode initialization
            if strParsed.startswith('#@ Invalid Ruleset'):
                strParsed = strParsed.split('.', 1)[1]
            if strParsed.strip() != '': #if we aren't dealing with an empty string
                if strParsed.startswith('|'): #if the ruleset mode is set as OR
                  self.RulesetMode = 'OR' #specify OR as ruleset mode
                rulesAndActions = strParsed.lstrip('|').split('=>',1) #split Rules and Actions
                self.ParseItemParameters(rulesAndActions[0], 'Rule') #Parse Rules
                self.ParseItemParameters(rulesAndActions[1], 'Action') #Parse Actions
        elif isinstance(strParameters, XElement):
            self.FromXML(strParameters)
        pass
        
    def ParseItemParameters(self, strRules, strRuleOrAction):
        """Parses strRules(string) to Rules Or Actions as specified by strRuleOrAction and adds it to this ruleset accordingly"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:ParseItemParameters(stringParameters, stringRuleOrAction)'
        parameters = strRules.split('> <') #split into individual rules or actions
        for parameter in parameters: #for each item in the created list
            if parameter.strip() != '': #if the item is not an empty string
                if strRuleOrAction == 'Rule': #if indicated as a Rule
                    self.Rules.Add(dmRule(self, parameter)) #create and add a dmRule instance to this Ruleset's Rules
                elif strRuleOrAction == 'Action': #if indicated as an Action
                    self.Actions.Add(dmAction(self, parameter)) #create and add a dmAction instance to this Ruleset's Actions
        pass
    
    def MeetsConditions(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:MeetsConditions(book)'
        bReturn = True
        if self.Rules.Count < 1:
            if dmGlobals.TraceGeneralMessages: print 'There are no rules defined.'
            return True
        if self.RulesetMode == 'OR': #if we are using OR mode
            if dmGlobals.TraceGeneralMessages: print 'Checking rules in OR Mode'
            if len(self.Rules) > 0: 
                bReturn = False #we need False to be default if we are in OR mode but only if there are rules present.
            for rule in self.Rules: #iterate over rules
                try:
                    if rule.Match(book): #we only need one match to decide if conditions are met in OR mode
                        bReturn = True #set return True as soon as a match found
                        break #and then exit iteration
                except Exception as er:
                    #report errors instead
                    bReturn = False
        else: #if we are using AND mode
            if dmGlobals.TraceGeneralMessages: print 'Checking rules in AND Mode'
            for rule in self.Rules: #iterate through Rules
                try:
                    if not rule.Match(book): # we only need one non-match to determine conditions are not met
                        bReturn = False #set return to False as soon as non-match found
                        break #and then exit iteration
                except Exception as er:
                    #report errors instead
                    bReturn = False
        return bReturn #return True or False

    def ApplyActions(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:ApplyActions(book)'
        strReport = ''
        for action in self.Actions:
            if dmGlobals.TraceGeneralMessages: print 'Applying Actions...'
            try:
                strTemp = action.Apply(book)
            except Exception as er:
                #report errors instead
                strTemp = ''
                strReport = '    An unexpected error occured in Action: ' + self.ToString() + System.Environment.NewLine
                strReport = strReport + '        Error: ' + er.message
            if strTemp != '':
                if strReport != '': strReport = strReport + System.Environment.NewLine
                if dmGlobals.TraceGeneralMessages: print 'Value was modified, adding info to report'
                strReport = strReport + strTemp
        if dmGlobals.TraceFunctionMessages: print 'Exiting Method: dmRuleset:ApplyActions(book)'
        return strReport

    def ProcessBook(self, book, bgwProcess):
        """Begins Processing of Book with this Ruleset"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:ProcessBook(book, backgroundWorker)'
        strReport = ''
        if dmGlobals.TraceGeneralMessages: print 'Checking rules...'
        if self.MeetsConditions(book): #if Rules meet conditions
            if dmGlobals.TraceGeneralMessages:
                print 'Book met all conditional rules'
                print 'Processing Ruleset: ' + self.Name
            #create a dictionary of values
            strTemp = self.ApplyActions(book)
            if strTemp != '': 
                strReport = System.Environment.NewLine + 'Book: ' + book.CaptionWithoutTitle + ' was touched. ' + self.ToString() + System.Environment.NewLine + strTemp
            
        return strReport

    def ToString(self):
        if dmGlobals.TraceFunctionMessages: print 'Method dmRuleset:ToString()'
        strReturn = 'Ruleset: ' + self.Name + ' ' + self.HumanizeRules()
        return strReturn

    def HumanizeRules(self):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:HumanizeRules()'
        strReturn = '('

        ruleCount = 0
        while ruleCount < len(self.Rules):
            strReturn = strReturn + self.Rules[ruleCount].ToString()
            ruleCount = ruleCount + 1
            if ruleCount < len(self.Rules): strReturn = strReturn + ' ' + self.RulesetMode + ' '

        strReturn = strReturn + ' => '

        actionCount = 0
        while actionCount < len(self.Actions):
            strReturn = strReturn + self.Actions[actionCount].ToString()
            actionCount = actionCount + 1

        strReturn = strReturn + ')'
        return strReturn

    def ToXML(self, elementName):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:ToXML(stringElementName)'
        baseElement = dmNode.ToXML(self, elementName)
        baseElement.Attribute['rulesetmode'] = self.RulesetMode
        for rule in self.Rules:
            baseElement.append(rule.XMLSerialize('rule'))
        for action in self.Actions:
            baseElement.append(action.XMLSerialize('action'))
        pass

    def FromXML(self, element):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRuleset:FromXML(xmlElement)'
        dmNode.FromXML(self, element)
        self.RulesetMode = element.Attribute(XName.Get('rulesetmode')).Value
        for rule in element.Elements(XName.Get('rule')):
            self.Rules.append(dmRule(self, rule))
        for action in element.Elements(XName.Get('action')):
            self.Actions.append(dmAction(self, action))
        pass

class dmParameters(dmNode):
    
    def getField(self):
        return self._Field
    def setField(self, strCompleteField):
        self.ParseField(strCompleteField)
    Field = property(getField, setField)

    def getModifier(self):
        return self._Modifier
    def setModifier(self, strModifier):
        self._Modifier = strModifier
    Modifier = property(getModifier, setModifier)

    def getValue(self):
        return self._Value
    def setValue(self, strValue):
        self._Value = strValue
    Value = property(getValue, setValue)

    @property
    def IsCustomField(self):
        return self.Field in dmGlobals.READONLYKEYS or not self.Field in dmGlobals.ALLOWEDVALS    

    @property       
    def IsValid(self):
        if dmGlobals.TraceFunctionMessages: print 'Property: dmParameters:IsValid'
        bReturn = True

        #validation for Actions
        if isinstance(self, dmAction):
            if (not self.Field in dmGlobals.ALLOWEDVALS):
                bReturn = False
            if not self.Modifier in dmGlobals.ValidValModifiers(self.Field):
                bReturn = False
        
        #validation for Rules
        elif isinstance(self, dmRule):
            if (not self.Field in dmGlobals.ALLOWEDVALS):
                bReturn = False
            if not self.Modifier in dmGlobals.ValidValModifiers(self.Field):
                bReturn = False

        #TODO: Determine if the value is valid
        if not ValueValid():
            bReturn = false
        return bReturn

    """base object for dmRule & dmAction instances"""
    def __init__(self, dmnparent, strParameters):
        """initializes a dmParameter instance"""
        dmNode.__init__(self, dmnparent, strParameters) #calls the base dmNode initializer to initialize further fields
        self.Field = '' #initializes the field
        self.Modifier = '' #initializes the modifier value
        self.Value = '' #initializes the value value
        
        if strParameters != None:
            if isinstance(strParameters, XElement):
                self.FromXML(strParameters)
            else:
                self.ParseParameters(strParameters)
        pass

    def ValueValid(self):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:ValueValid()'
        bReturn = True
        if self.Field in dmGlobals.FIELDSNUMERIC:
            #check that string can be converted to this type
            try:
                dmGlobals.StringToFloat(self.Value)
            except:
                bReturn = False
        if self.Field in dmGlobals.FIELDSDATETIME:
            #check that string can be converted to this type
            try:
                dmGlobals.StringToDate(self.Value)
            except:
                bReturn = False
        if self.Field in dmGlobals.FIELDSLANGUAGEISO:
            #TODO: ReadLanguages and ISO abbreviations
            #check that string can be converted to this type
            try:
                pass
            except:
                pass
        if self.Field in dmGlobals.FIELDSBOOL:
            #check that string can be converted to this type
            try:
                dmGlobals.StringToBool(self.Value)
            except:
                bReturn = False
        if self.Field in dmGlobals.FIELDSMANGAYESNO:
            #check that string can be converted to this type
            try:
                dmGlobals.StringToMangaYesNo(self.Value)
            except:
                bReturn = False
        if self.Field in dmGlobals.FIELDSYESNO:
            #check that string can be converted to this type
            try:
                dmGlobals.StringToYesNo(self.Value)
            except:
                bReturn = False
        if self.Field in dmGlobals.FIELDSSTRING or self.Field in dmGlobals.FIELD or self.Field in dmGlobals.FIELDSCUSTOM:
            if not self.Field in dmGlobals.FIELDSMULTILINE:
                #checks for carriage return info in string values that do not support new lines
                if '{newline}' in self.Value:
                    bReturn = False

        return bReturn;

    def ParseParameters(self, strParameters):
        """Parses the string containing info for the parameters"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:ParseParameters(objParameters)'
        if isinstance(strParameters, str):
            item = strParameters.strip() #strip whitespace from front of string
        
            item = item.lstrip('<') #remove all instances '<' from front of string
            item = item.rstrip('>') #remove all instances '>' from back of string
        
            tmpParameters = item.split('.',1) #results in [field, modifier&value]
            self.ParseField(tmpParameters[0]) #sets complete field from field value in created list
            modfierAndValue = tmpParameters[1].split(':',1) #results in [modifier, value]
        
            self.Modifier = modfierAndValue[0] #set the modifier
            if len(modfierAndValue) > 1: #if a value is present
                self.Value = modfierAndValue[1] #set the value accordingly
            else:
                self.Value = '' #otherwise set Value to empty string for safety purposes

        elif isinstance(strParameters, XElement):
            self.FromXML(strParameters)
        else:
            print 'could not parse Parameter Info' + strParameter
        pass

    def FieldConvert(self, strValue, strField=None):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:FieldConvert(stringValue, stringFieldName)'
        
        FieldValue = self.Field
        if strField != None:
            FieldValue = strField

        theVal = strValue
        try:
            if FieldValue in dmGlobals.ALLOWEDVALS:
                if FieldValue in dmGlobals.FIELDSLIST and not dmGlobals.IsList(strValue):
                    theVal = filter(None, strValue.split(dmGlobals.CRLISTDELIMITER))
                elif FieldValue in dmGlobals.FIELDSBOOL and not dmGlobals.IsBool(strValue):
                    theVal = dmGlobals.StringToBool(strValue)
                elif FieldValue in dmGlobals.FIELDSDATETIME and not dmGlobals.IsDateTime(strValue):
                    theVal = dmGlobals.StringToDate(strValue)
                elif FieldValue in dmGlobals.FIELDSNUMERIC and not dmGlobals.IsFloat(strValue):
                    theVal = dmGlobals.StringToFloat(strValue)
                elif FieldValue in dmGlobals.FIELDSMANGAYESNO and not dmGlobals.IsMangaYesNo(strValue):
                    theVal = dmGlobals.StringToMangaYesNo(strValue)
                elif FieldValue in dmGlobals.FIELDSYESNO and not dmGlobals.IsYesNo(strValue):
                    theVal = dmGlobals.StringToYesNo(strValue)
                elif FieldValue in dmGlobals.FIELDSPSUEDONUMERIC and not isinstance(strValue,str):
                    try:                    
                        theVal = strValue.ToString()
                    except:
                        pass
            #otherwise just return the value
        except Exception as ex:

            pass
        return theVal 
		
    def GetStringValue(self, book, strField):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParamaters.GetFieldValue(book, strFieldName)'
        objReturn = None
        FieldValue = strField

        objReturn = dmGlobals.ToString(getattr(book, strField))

        return objReturn

    def GetFieldValue(self, book, strFieldName=None):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:GetFieldValue(book, strFieldName)'
        objReturn = None
        FieldValue = self.Field
        if strFieldName != None:
            FieldValue = strFieldName
        
        if dmGlobals.TraceGeneralMessages: print 'Retrieving value for ' + FieldValue + ' field in comic: ' + book.CaptionWithoutTitle #debug Info
        
        if FieldValue in dmGlobals.FIELDSLIST:
            objReturn = self.GetList(book, FieldValue)
        elif not FieldValue in dmGlobals.ALLOWEDVALS and not FieldValue in dmGlobals.ALLOWEDKEYS:
            objReturn = self.GetCustomField(book, FieldValue)            
        else:
            objReturn = getattr(book, FieldValue)

        
        if dmGlobals.TraceGeneralMessages: 
            print dmGlobals.ToString(objReturn)        
            print
        return objReturn

    def GetList(self, book, strFieldName):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:GetList(book, strFieldName)'
        strList = getattr(book, strFieldName)
        if strList == None or strList == '': 
            strList = []
        else:
            strList = strList.split(dmGlobals.CRLISTDELIMITER)
        return strList

    def GetCustomField(self, book, strFieldName):
        print 'Method: dmParameters:GetCustomField(book, strCustomFieldName)'
        strTemp = book.GetCustomValue(strFieldName)
        if strTemp == None:
            strTemp = ''
        return strTemp
       
    def ParseField(self, strCompleteField=''):
        """Sets Field & CustomField values properly"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:ParseField()'
        
        if strCompleteField.startswith('Custom'): # if CustomField begins with 'Custom'
            tmpRegex = Regex("Custom\((.*?)\)")
            self._Field = tmpRegex.Match(strCompleteField).Groups[1].Value #set the Field Value
        else: #otherwise
            self._Field = strCompleteField #Field value == CompleteField value            
        pass
    
    def ToXML(self, elementName):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:ToXML(stringElementName)'
        baseElement = XElement(elementName)
        baseElement.Add(XAttribute(XName.Get('field'), self.Field))
        baseElement.Add((XName.Get('modifier'), self.Modifier))
        baseElement.Add(XAttribute(XName.Get('value'), self.Value))
        return baseElement

    def FromXML(self, element):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:FromXML(xmlElement)'
        self.Field = element.Attribute(XName.Get('field')).Value
        self.Modifier = element.Attribute(XName.Get('modifier')).Value
        self.Value = element.Attribute(XName.Get('value')).Value

    def ReplaceReferenceStrings(self, strValue, book):
        """Replaces references to other fields and newline and tab references"""
        if dmGlobals.TraceFunctionMessages: print 'dmAction:ReplaceReferenceStrings(self, strValue, book)'
        strNewValue = strValue
                
        strNewValue = strNewValue.replace('{newline}', System.Environment.NewLine)
        strNewValue = strNewValue.replace('{tab}', '    ')
        
        #find field (including custom) references and replace
        for x in Regex.Matches(strNewValue, "{([^},]{3,}?)}"):
            if x.Groups[1].Value in dmGlobals.FIELDSSTRING:
                strNewValue = strNewValue.Replace(x.Groups[0].Value, self.GetStringValue(book, x.Groups[1].Value))            
            else:
                strNewValue = strNewValue.Replace(x.Groups[0].Value, dmGlobals.ToString(self.GetFieldValue(book, x.Groups[1].Value)))         

        return strNewValue

    def ToString(self):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmParameters:ToString()'
        strReturn = self.Field + ' ' + self.Modifier.upper() + ' \'' + self.Value + '\''
        return strReturn

class dmRule(dmParameters):
    """defines a restriction on whether or not defined actions should be applied"""
    def __init__(self, dmnparent, strParameters):
        """initializes a dmRule instance"""
        if dmGlobals.TraceFunctionMessages: print 'dmRule constructor: dmRule(dmNodeParent, objParameters)'
        dmParameters.__init__(self, dmnparent, strParameters) #call initialization done in the dmParameters base instance
        pass

    def Match(self, book):
        """Determines if the rule matches the book file (returns True or False)"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Match(book)'
        return getattr(self, self.Modifier)(book) #sends the book to the designated (by self.Modifier) function to determine if the rule matches

    def Is(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Is(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.FieldConvert(self.ReplaceReferenceStrings(self.Value, book) ,self.Field) #value to compare
        
        if self.Field in dmGlobals.FIELDSLIST: #deal with list items as individual items
            
            if len(compareValue) == len(getValue): #only continue if lists are same legnth
                count = 0
                for item in compareValue: #iterate through compare list items
                    for val in getValue: #iterate through book list items
                        if val.lower() == item.lower(): #compare lowercase list items from book (val) to compare list items (item)
                            count = count + 1 #if match increment count
                if count == len(getValue): #if count ends up equal between book list items and compare list items
                    return True #set true
        else:
            if isinstance(getValue, str):
                if getValue.lower() == compareValue.lower():
                    return True
            else:
                if getValue == compareValue: #if values match 
                    return True #set true
        
        return False #if everything else fails set false

    def Not(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Not(book)'
        return not self.Is(book) #return inverse of 'Is(book)'

    def IsAnyOf(self, book):
        """Available for string languageISO, psuedonumeric, and numeric"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:IsAnyOf(book)'
                
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER)  #value to compare as list
       
        for word in compareValue:
            if isinstance(getValue, str): #if dealing with string
                if getValue.lower() == word.lower(): #compare lowercase
                    return True
            if getValue == self.FieldConvert(word, self.Field):
                    return True
        return False

    def NotIsAnyOf(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotIsAny(book)'
        return not self.IsAnyOf(book)

    def Contains(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Contains(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book)  #value to compare
                
        if self.Field in dmGlobals.FIELDSLIST: #search as string list            
            for check in getValue:
                if compareValue.lower() in check.lower():
                    return True
        else: #search as string
            if compareValue.lower() in getValue.lower():
                return True
        return False

    def NotContains(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotContains(book)'
        return not self.Contains(book)
    
    def ContainsAnyOf(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:ContainsAnyOf(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER)  #value to compare
                
        for compareItem in compareValue:
            if self.Field in dmGlobals.FIELDSLIST: #compare list against list                
                for getItem in getValue: #compare list items as lowercase
                    if compareItem.lower() in getItem.lower():
                        return True #return true at first instance of match
            else: #compare list against string
                if compareItem.lower() in getValue.lower(): #compare string item against list item
                    return True #return true at first instance of match
        return False #all else failing return false
    
    def NotContainsAnyOf(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotContainsAnyOf(book)'
        return not self.ContainsAnyOf(book)
    
    def ListContains(self, book):
         """Only applicable with string and list"""
         if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Contains(book)'

         for check in getValue:
             if check.lower() == compareValue.lower():
                 return True
    
    def NotListContains(self, book):
        return not self.ListContains(book)
    
    def ListContainsAnyOf(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:ContainsAnyOf(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER)  #value to compare
                
        for compareItem in compareValue:
            if self.Field in dmGlobals.FIELDSLIST: #compare list against list                
                for getItem in getValue: #compare list items as lowercase
                    if compareItem.lower() in getItem.lower():
                        return True #return true at first instance of match
            else: #compare list against string
                if compareItem.lower() in getValue.lower(): #compare string item against list item
                    return True #return true at first instance of match
    
    def NotListContainsAnyOf(self, book):
        return not self.ListContainsAnyOf(book)
    
    def ListContainsAllOf(self, book):

        pass
    
    def ListContainsAllOf(self, book):
        return not self.ListContainsAllOf(book)
        pass



    def ContainsAllOf(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:ContainsAllOf(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER)  #value to compare

        all = True 
        for compareItem in compareValue:
            if self.Field in dmGlobals.FIELDSLIST: #compare list against list                
                for getItem in getValue: #compare list items as lowercase
                    all &= compareItem.lower() in getItem.lower()
            else: #compare list against string
                all &= compareItem.lower() in getValue.lower() #compare string item against list item
        return all

    def NotContainsAllOf(self, book):
        """Only applicable with string and list"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotContainsAllOf(book)'
        return not self.ContainsAllOf(book)

    def StartsWith(self, book):
        """Only applicable with string"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:StartsWith(book)'
                
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book)  #value to compare
        
        return getValue.lower().startswith(compareValue.lower())

    def NotStartsWith(self, book):
        """Only applicable with string"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotStartsWith(book)'
        return not self.StartsWith(book)

    def StartsWithAnyOf(self, book):
        """Only applicable with string"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:StartsWithAnyOf(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER)  #value to compare
        
        for compareItem in compareValue: #compare each item until truth found 
            if getValue.lower().startswith(compareItem.lower()): #check if list item at the beginning of string
                return True # return true at first instance of match

        return False

    def NotStartsWithAnyOf(self, book):
        """Only applicable with string"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotNotStartsWithAnyOf(book)'
        return not self.StartsWithAnyOf(book)

    def Greater(self, book):
        """Only applicable with numeric, psuedo numeric, and date"""        
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Greater(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.FieldConvert(self.Value, self.Field)  #value to compare

        if self.Field in dmGlobals.FIELDSNUMERIC:
            try:
                compareValue = dmGlobals.StringToFloat(compareValue)
                return getValue > compareValue
            except:
                raise Exception('could not convert \'' + self.Value + '\'  to Float')
        elif self.Field in dmGlobals.FIELDSPSUEDONUMERIC:
            count = 0
            prefixGet = ''
            prefixCompare = ''
            numberCompare = ''
            numberGet = ''
            suffixGet = ''
            suffixCompare = ''
            
            #seperate prefixes and suffixes
            while count < len(getValue) and not getValue[count].isdigit():
                prefixGet = prefixGet + getValue[count]
                count = count + 1
            while count < len(getValue) and getValue[count].isdigit():
                numberGet = numberGet + getValue[count]
                count = count + 1
            while count < len(getValue):
                suffixGet = suffixGet + getValue[count]
                count = count + 1

            count = 0
            
            while count < len(compareValue) and not compareValue[count].isdigit():
                prefixCompare = prefixCompare + compareValue[count]
                count = count + 1
            while count < len(compareValue) and compareValue[count].isdigit():
                numberCompare = numberCompare + compareValue[count]
                count = count + 1
            while count < len(compareValue):
                suffixCompare = suffixCompare + compareValue[count]
                count = count + 1

            try:
                if prefixCompare == prefixGet: #if prefixes match
                    if numberGet == numberCompare:
                        return suffixGet > suffixCompare
                    else:
                        return dmGlobals.StringToFloat(numberGet) > dmGlobals.StringToFloat(numberCompare)
                else: #return comparison of prefixes
                    return prefixGet > prefixCompare

                return getValue > compareValue
            except:
                raise Exception('could not convert \'' + self.Value + '\'  to Float')

        elif self.Field in dmGlobals.FIELDSDATETIME:
            try:
                return getValue > compareValue
            except:
                raise Exception('could not convert \'' + self.Value + '\'  to Date')

        return False

    def GreaterEq(self, book):
        """Only applicable with numeric, psuedo numeric, and date"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:GreaterEq(book)'
        return self.Greater(book) or self.Is(book)

    def Less(self, book):
        """Only applicable with numeric, psuedo numeric, and date"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Less(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #get Value from book
        compareValue = self.FieldConvert(self.Value, self.Field)  #value to compare

        if self.Field in dmGlobals.FIELDSNUMERIC:
            try:
                compareValue = dmGlobals.StringToFloat(compareValue)
                return getValue < compareValue
            except:
                raise Exception('could not convert \'' + self.Value + '\'  to Float')
        elif self.Field in dmGlobals.FIELDSPSUEDONUMERIC:
            count = 0
            prefixGet = ''
            prefixCompare = ''
            numberCompare = ''
            numberGet = ''
            suffixGet = ''
            suffixCompare = ''
            
            #seperate prefixes and suffixes
            while count < len(getValue) and not getValue[count].isdigit():
                prefixGet = prefixGet + getValue[count]
                count = count + 1
            while count < len(getValue) and getValue[count].isdigit():
                numberGet = numberGet + getValue[count]
                count = count + 1
            while count < len(getValue):
                suffixGet = suffixGet + getValue[count]
                count = count + 1

            count = 0
            
            while count < len(compareValue) and not compareValue[count].isdigit():
                prefixCompare = prefixCompare + compareValue[count]
                count = count + 1
            while count < len(compareValue) and compareValue[count].isdigit():
                numberCompare = numberCompare + compareValue[count]
                count = count + 1
            while count < len(compareValue):
                suffixCompare = suffixCompare + compareValue[count]
                count = count + 1

            try:
                if prefixCompare == prefixGet: #if prefixes match
                    if numberGet == numberCompare: #and number matches
                        return suffixGet < suffixCompare #return suffix comparison
                    else:
                        return dmGlobals.StringToFloat(numberGet) < dmGlobals.StringToFloat(numberCompare) #return Number comparision
                else: #return comparison of prefixes
                    return prefixGet < prefixCompare
            except:
                raise Exception('could not convert \'' + self.Value + '\'  to Float')

        elif self.Field in dmGlobals.FIELDSDATETIME:
            try:
                return getValue < compareValue
            except:
                raise Exception('could not convert \'' + self.Value + '\'  to Date')

        return False

    def LessEq(self, book):
        """Only applicable with numeric, psuedo numeric, and date"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:LessEq(book)'
        return self.Less(book) or self.Is(book)
        
    def Range(self, book):
        """Only applicable with numeric, psuedo numeric, and date"""
        if dmGlobals.TraceFunctionMessages: print 'Method dmRule:Range(book)'

        getValue = self.GetFieldValue(book, self.Field)
        if self.Field in dmGlobals.FIELDSPSUEDONUMERIC and isinstance(getValue, str):
            getValue = dmGlobals.StringToFloat(getValue)
        
        minVal = self.Value.split(dmGlobals.DMLISTDELIMITER)[0]
        maxVal = self.Value.split(dmGlobals.DMLISTDELIMITER)[1]
        
        if (self.Field in dmGlobals.FIELDSNUMERIC) or (self.Field in dmGlobals.FIELDSPSUEDONUMERIC):
            minVal = dmGlobals.StringToFloat(minVal)
            maxVal = dmGlobals.StringToFloat(maxVal)
        elif self.Field in dmGlobals.FIELDSDATETIME:
            minVal = System.DateTime.Parse(minVal)
            maxVal = System.DateTime.Parse(maxVal + ' 23:59:59')
        if getValue >= minVal and getValue <= maxVal:
            return True
        return False
    
    def NotRange(self, book):
        """Only applicable with numeric, psuedo numeric, and date"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotRange(book)'
        return not Range(book)

    def RegEx(self, book):
        """Only applicable with string"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:RegEx(book)'

        getValue = self.GetFieldValue(book, self.Field)
        compareValue = self.ReplaceReferenceStrings(self.Value, book)

        regExp = Regex(compareValue, RegexOptions.Singleline | RegexOptions.IgnoreCase)

        return regExp.Match(getValue).Success

    def NotRegEx(self, book):
        """Only applicable with string"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:NotRegEx(book)'
        return not self.RegEx(book)

class dmAction(dmParameters):
    def __init__(self, dmnparent, strParameters):
        if dmGlobals.TraceFunctionMessages: print 'dmAction constructor: dmAction(dmRulesetParent, objParameters)'
        dmParameters.__init__(self, dmnparent, strParameters)
        pass

    def Apply(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:Apply(book)'
        strReport = getattr(self, self.Modifier)(book) #send book to function specified by Modifier
        return strReport
    
    def SetFieldValue(self, book, newValue, strField=None):
        """Determines the proper write to book technique (Standard or Custom Field) and applies value"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:SetValue(book, objNewValue, stringFieldName)'

        FieldValue = self.Field
        
        if strField != None:
            FieldValue = strField

        previousVal = self.GetFieldValue(book, FieldValue)

        newVal = newValue

        strReport = ''            
        if FieldValue in dmGlobals.FIELDSLIST:
            if dmGlobals.SortLists:
                newVal.sort()
            newVal = dmGlobals.CRLISTDELIMITER.join(newVal)
            previousVal = dmGlobals.CRLISTDELIMITER.join(previousVal)
        
        if FieldValue in dmGlobals.ALLOWEDVALS:
            try:
                if FieldValue in dmGlobals.FIELDSNUMERIC:
                    setattr(book, FieldValue, dmGlobals.StringToFloat(newVal)) #convert to float
                elif FieldValue in dmGlobals.FIELDSPSUEDONUMERIC:
                    setattr(book, FieldValue, dmGlobals.ToString(newVal))
                else:
                    setattr(book, FieldValue, newVal)
                #prepare the report
                strReport = '    Field: ' + FieldValue + '    Action: ' + self.ToString()
                strReport = strReport + System.Environment.NewLine + '        Previous Value: ' + dmGlobals.ToString(previousVal)
                strReport = strReport + System.Environment.NewLine + '        New Value: ' + dmGlobals.ToString(newVal) + '\r\n'
            except Exception as er:
                #report errors instead
                strReport = '    An unexpected error occured in Action: ' + self.ToString() + '    Parent Ruleset : ' + self.Parent.Name + System.Environment.NewLine
                if isinstance(er, dmConversionError):
                    strReport = strReport + '        Error: ' + er.msg + System.Environment.NewLine
                else:
                    strReport = strReport + '        Error: ' + er.message + System.Environment.NewLine
                pass
        else:
            self.SetCustomField(book, FieldValue, newVal)
            #prepare the report
            if strReport != '': strReport = System.Environment.NewLine
            strReport = '    CustomField: ' + self.Field + '    Action: ' + self.ToString()
            strReport = strReport + System.Environment.NewLine + '        Previous Value: ' + dmGlobals.ToString(previousVal)
            strReport = strReport + System.Environment.NewLine + '        New Value: ' + dmGlobals.ToString(newVal)
        return strReport

    def SetCustomField(self, book, strCustomFieldName, strNewValue):
        """Sets 'CustomField' value of book to strNewValue"""
        if dmGlobals.TraceFunctionMessages: print 'SetCustomField(book, stringFieldName, stringNewValue)'
        book.SetCustomValue(strCustomFieldName, strNewValue)
        pass
    
    
    def GetAppendedField(self, strFieldName, book, strAppendString):
        objReturn = self.GetFieldValue(book, strFieldName)
        if strFieldName in dmGlobals.FIELDSLIST:
            objReturn.append(strAppendString)
        elif strFieldName in dmGlobals.FIELDSMULTILINE:
            objReturn = objReturn + System.Environment.NewLine + strAppendString
        else:
            objReturn = objReturn + ' ' + strAppendString
        return objReturn
       
    def SetValue(self, book):
        """valid with all action value types"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:SetValue(book)'
        if dmGlobals.TraceGeneralMessages: print 'book = ' + book.CaptionWithoutTitle
        strReport = ''

        setValue = self.ReplaceReferenceStrings(self.Value, book) #get new Value from local value replacing reference strings
        
        setValue = self.FieldConvert(setValue, self.Field) #convert setValue to proper object class

        strReport = self.SetFieldValue(book, setValue)

        return strReport

    def Add(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmRule:Add(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #copy current value
        setValue = self.ReplaceReferenceStrings(self.Value,book).split(dmGlobals.DMLISTDELIMITER) #copy value replacing book variables with their values
            
        strReport = ''
        newVal = getValue

        if self.Field in dmGlobals.FIELDSLIST:
            addItem = True
            for value in setValue:
                for existingItem in newVal:
                    if value.lower() == existingItem.lower():
                        addItem = False
                        break
            if addItem:
                newVal.Add(value)
        else: #since this is only a valid modifier for list and string assume string            
            for item in setValue:
                newVal = newVal + item
                
        strReport = self.SetFieldValue(book, newVal) #finally set the new value
        return strReport
        
    def Remove(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:Remove(book)'
        
        getValue = self.GetFieldValue(book, self.Field) #copy current value
        setValue = self.ReplaceReferenceStrings(self.Value,book).split(dmGlobals.DMLISTDELIMITER) #copy value replacing book variables with their values
        
        strReport = ''
        newVal = ''
        
        #set values for list items
        if self.Field in dmGlobals.FIELDSLIST: #if the type of field is a list
            tmpList = [] #create a list to transfer values to
            
            for item in getValue: #iterate over the book's list items
                addItem = True
                for val in setValue: #iterate through the values to remove
                    if val.lower() == item.lower(): #compare value to remove to book's list item if it does not match
                        addItem = False
                        break
                if addItem:
                    tmpList.append(item) #add item to list
                                    
            setValue = tmpList
        else: #if it's not a list item consider it a string (since only strings and lists have this modifier available)
            for val in setValue: #iterate through list of values to remove
                newValue = getValue
                if val:
                    while  val.lower() in newValue.lower(): #as long as string contains the value to remove
                        idx = newValue.lower().find(val.lower()) #find the index of the value to remove
                        newValue = newValue.Remove(idx, len(val)) #remove len(val) characters starting from idx

            setValue = newValue
            
        strReport = self.SetFieldValue(book, setValue)
            
            
        return strReport #return Action Report

    def Replace(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:Replace(book)'
        
        getValue = self.GetFieldValue(book, self.Field)
        setValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER)
        newValue = getValue


        finditem = setValue[0]
        replaceitem = setValue[1]

        if self.Field in dmGlobals.FIELDSLIST:
            oldList = self.GetFieldValue(book, self.Field)
            newList = []
            if not dmGlobals.COMPARE_CASE_SENSITIVE:
                for getItem in getValue:
                    if getItem.lower() == finditem.lower():
                        newList.Add(replaceitem)
                        break 
                    else:
                        newList.Add(getItem)
            else:
                for getItem in getValue:
                    if getItem == finditem:
                        newList.Add(replaceitem)
                        break 
                    else:
                        newList.Add(getItem)           
            newValue = newList
    
        else:
            idx = 0; idx2 = -1
            if not dmGlobals.COMPARE_CASE_SENSITIVE:
                while finditem.lower() in newValue.lower():
                    idx = newValue.lower().find(finditem.lower()) #find the index of the value to replace
                    newValue = newValue.Remove(idx, len(finditem))
                    newValue = newValue.Insert(idx, replaceitem)
                    if idx2 == idx:
                        break
                    idx2 = idx
            else:
                while finditem in newValue:
                    idx = newValue.find(finditem) #find the index of the value to replace
                    newValue = newValue.Remove(idx, len(finditem))
                    newValue = newValue.Insert(idx, replaceitem) 
                    if idx2 == idx:
                        break
                    idx2 = idx
            
        strReport = self.SetFieldValue(book, newValue)

        
        return strReport

    def Calc(self, book):
        """valid for numeric and psuedonumeric"""
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction.Calc(book)'
                                                        
        setValue = self.ReplaceReferenceStrings(self.Value, book)
        
        try:
            myVal = eval(setValue)
        except:
            myVal = self.FieldConvert(setValue, self.Field) #convert setValue to proper object class
        
        strReport = self.SetFieldValue(book, myVal)
            
        return strReport

    def RegexReplace(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:RegexReplace(book)'
        
        getValue = self.GetFieldValue(book, self.Field)
        setValue = self.ReplaceReferenceStrings(self.Value, book).split(dmGlobals.DMLISTDELIMITER, 1)

        strReport = ''

        setPattern = setValue[0]
        setFormat = setValue[1]
                
        RegExp = Regex(setPattern, RegexOptions.IgnoreCase | RegexOptions.Singleline)
        
        myString = getValue         
        myString = RegExp.Replace(myString, setFormat)         
        
        strReport = self.SetFieldValue(book, myString)
            
        return strReport
    
    def RegExVarReplace(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:RegexVarReplace(book)'
        myString = self.GetFieldValue(book, self.Field) #get the value of the Field in the book
        myVal = self.ReplaceReferenceStrings(self.Value, book) #replace reference strings on the proposed value

        strReport = '' #initialize report

        
        RegExp = Regex(myVal, RegexOptions.IgnoreCase) #compile the Regex

        matchItem = RegExp.Match(myString) #get the match
        if matchItem.Success:
            if dmGlobals.TraceGeneralMessages: print 'Book: ' + book.CaptionWithoutTitle + ' field ' + self.Field + ' matched Regex ' + myVal  #print Debug Info
            if dmGlobals.TraceGeneralMessages: print '    book.' + self.Field + '= ' + dmGlobals.ToString(myString)
            if dmGlobals.TraceGeneralMessages: print '    Regex Match = ' + matchItem.Groups[0].Value
                

        #iterate over capture names and apply
        for groupName in RegExp.GetGroupNames():
            if dmGlobals.TraceGeneralMessages: print 'attempting to apply values to specified fields. WARNING: any unnamed captures will cause an error'
            try:
                if groupName != '0': #eliminate possible error of group zero being used (group zero is the whole match text)
                    strFieldName = groupName #get fieldname that's being changed
                    strNewValue = matchItem.Groups[groupName].Value #get the text that will replace the field
                    
                    strReport = strReport + self.SetFieldValue(book, strNewValue, strFieldName) #replace the field
            except Exception as er:

                pass
        return strReport

    def RegExVarAppend(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:RegexVarAppend(book)'

        
        myString = self.GetFieldValue(book, self.Field) #get the value of the Field in the book
        myVal = self.ReplaceReferenceStrings(self.Value, book) #replace reference strings on the proposed value

        strReport = '' #initialize report

        
        RegExp = Regex(myVal, RegexOptions.IgnoreCase) #compile the Regex

        matchItem = RegExp.Match(myString) #get the match
        if matchItem.Success:
            if dmGlobals.TraceGeneralMessages: print 'Book: ' + book.CaptionWithoutTitle + ' field ' + self.Field + ' matched Regex ' + myVal  #print Debug Info
            if dmGlobals.TraceGeneralMessages: print '    book.' + self.Field + '= ' + dmGlobals.ToString(myString)
            if dmGlobals.TraceGeneralMessages: print '    Regex Match = ' + matchItem.Groups[0].Value
                

        #iterate over capture names and apply
        for groupName in RegExp.GetGroupNames():
            if dmGlobals.TraceGeneralMessages: print 'attempting to apply values to specified fields. WARNING: any unnamed captures will cause an error'
            try:
                if groupName != '0': #eliminate possible error of group zero being used (group zero is the whole match text)
                    strFieldName = groupName #get fieldname that's being changed
                    strNewValue = ''
                    
                    strNewValue = self.GetAppendedField(strFieldName, book, matchItem.Groups[groupName].Value) #get the text that will replace the field
                    strOldValue = self.GetFieldValue
                    strReport = strReport + self.SetFieldValue(book, strNewValue, strFieldName) #replace the field
                    
            except Exception as er:

                pass
        return strReport

   
    def RemoveLeading(self, book):
        if dmGlobals.TraceFunctionMessages: print 'Method: dmAction:RemoveLeading(book)'
        
        myString = self.GetFieldValue(book)
        myVal = self.ReplaceReferenceStrings(self.Value, book)

        if myString.lower().startswith(myVal.lower()):
            myString = myString.Remove(0, len(myVal))

        strReport = self.SetFieldValue(book, myString)

        return strReport
