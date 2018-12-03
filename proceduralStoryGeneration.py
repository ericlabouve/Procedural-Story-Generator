import sys
from random import choice

from tokenizer import Statement, isOptElemKey, OptionalElement, ChooseElement, OrElement, Element, OverElement, reduceSpaces
from sparqlBackend import getPersonInfo, doesWikiPageExist, getCityInfo, lenCityDict

STATEMENT_TYPE = 0
STATEMENT_PRECONDITION = 1
STATEMENT_VALUE_LIST = 2

PERSON_DICT = 0
CITY_DICT = 1


def main():
    contextDict = getContext()
    print("Finished getting context. Assembling story...")
    statementList = tokenizeFile(sys.argv)
    print(str(contextDict) + "\n\n\n\n\n\n\n" + str(statementList))
    putStoryTogether(contextDict, statementList)

def getContext():
    personDict = getPersonDict()
    cityDict = getCityDict()

    return [personDict, cityDict]

def tokenizeFile(argv):
    if len(argv) == 2:
        grammar = open(argv[1], "r")

        statementList = []
        for line in grammar: #lines:
            line = line.strip()
            if len(line) > 0:
                statementList.append(Statement(line))
    else:
        printf("Please include the filename of the grammar as an arguement")
        exit()

    return statementList

def putStoryTogether(contextDict, statementList):
    rootStatement, statementDict = parseStatementListToDict(statementList)
    
    print(resolveStatement(rootStatement, statementDict, contextDict))

def parseStatementListToDict(statementList):
    rootStatement = None
    statementDict = {}

    for statement in statementList:
        if rootStatement is None:
            rootStatement = statement.key.elemName

        precondition = statement.key.precondition if type(statement.key) is OptionalElement else ""
        statementDict[statement.key.elemName] = [type(statement.key), precondition, statement.value]

    return rootStatement, statementDict

def resolveStatement(resolve: str, statementDict, contextDict) -> str:
    statement = ""

    if resolve in statementDict:
        if type(statementDict[resolve][STATEMENT_TYPE]) is str:
            statement = statementDict[resolve][STATEMENT_VALUE_LIST][0]
        elif statementDict[resolve][STATEMENT_TYPE] is not OptionalElement or preconditionValid(statementDict[resolve][STATEMENT_PRECONDITION], statementDict, contextDict):
            statementValues = statementDict[resolve][STATEMENT_VALUE_LIST] 

            if type(statementValues) is not list:
                statementValues = [statementValues]

            resolvedStatements = []
            if type(statementValues[0]) is ChooseElement:
                statementValues = expandChoose(statementValues[0], statementDict, contextDict)
            for element in statementValues:
                if type(element) is OptionalElement or type(element) is Element:
                    resolvedStatements.append(resolveStatement(element.elemName, statementDict, contextDict))
                else:
                    resolvedStatements.append(element)

            statement += assembleElements(resolvedStatements, statementDict, contextDict)
        statementDict[resolve][STATEMENT_VALUE_LIST]  = statement
    elif resolve in contextDict[PERSON_DICT]:
        if contextDict[PERSON_DICT][resolve]:
            statement = choice(contextDict[PERSON_DICT][resolve])
    elif resolve in contextDict[CITY_DICT]:
        if contextDict[CITY_DICT][resolve]:
            statement = choice(contextDict[CITY_DICT][resolve])
    else:
        raise SyntaxError('Statement ' + str(resolve) + ' is not specified or able to be looked up from context')

    return statement

def assembleElements(statementValues, statementDict, contextDict):
    orStatement = False
    resolvedStatements = []

    for element in statementValues:
        if type(element) is OrElement:
            orStatement = True
            statementValues.remove(element)
        elif type(element) is str:
            resolvedStatements.append(element)
        else:
            statement = resolveStatement(element.elemName, statementDict, contextDict)
            if statement is not "":
                resolvedStatements.append(statement)

    if orStatement:
        statement = choose(statementValues)
    else:
        statement = resolvedStatements.join(" ")

    return statement

class condNode:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

    def evalTree(self):
        nodeTrue = False

        if type(self.value) is bool:
            nodeTrue = self.value
        elif self.value == "\AND":
            nodeTrue = self.left.evalTree() and self.right.evalTree()
        elif self.value == "\OR":
            nodeTrue = self.left.evalTree() or self.right.evalTree()

        return nodeTrue

    def __str__(self):
        return "(" + str(self.left) + " " + str(self.value) + " " + str(self.right) + ")"

    def hasAll(self):
        return self.value is not None and self.left is not None and self.right is not None

    def hasLeft(self):
        return self.value is not None and self.left is not None
                

def preconditionValid(preconditionList, statementDict, contextDict):
    precValid = False
    stack = []
    rootNode = None
    for condition in preconditionList.split():
        if condition != "\AND" and condition != "\OR":
            validCondition = (resolveStatement(condition, statementDict, contextDict) != "")
            if rootNode is None:
                rootNode = condNode(validCondition)
            else:
                rootNode.right = condNode(validCondition)
        else:
            tmpNode = rootNode
            rootNode = condNode(condition, tmpNode)
    precValid = rootNode.evalTree()

    return precValid

def getPersonDict():
    personDict = {}

    while not personDict: # Check if personDict is empty
        personName = input("Please enter a famous person's name: ").title().replace(" ", "_")
        # Capitolize first letter of each word and make cammel case for easier parsing of wikipedia
        print("Retrieving information, one moment...")
        personDict = getPersonInfo(personName)

        if len(personDict) <= 1:
            print("No info was found on " + personName.replace("_", " ") + ", please chose another")

    return personDict

def getCityDict():
    cityDict = {}

    while not cityDict: # Check if cityDict is empty
        cityName = input("Please enter a well known city: ").title().replace(" ", "_")
        stateName = input("Is this city located in America?\nIf so, please enter the state/province. Otherwise, please press enter: ").title().replace(" ", "_")
        page1 = cityName + ",_" + stateName
        page2 = cityName
        # Get DBPedia info if wiki page exists. 
        # Need to query both pages bec wikipedia has inconsistent naming conventions
        print("Retrieving information, one moment...")
        for page in [page1, page2]:
            if doesWikiPageExist(page):
                tempCityDict = getCityInfo(page)
                if lenCityDict(tempCityDict) > lenCityDict(cityDict):
                   cityDict = tempCityDict

        if len(cityDict) <= 1:
            print("No info was found on " + cityName.replace("_", " ") + ", please chose another")

    return cityDict

if __name__ == "__main__":
    main()
