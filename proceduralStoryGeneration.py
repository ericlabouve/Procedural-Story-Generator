import sys

from tokenizer import Statement, isOptElemKey, OptionalElement, ChooseElement
from sparqlBackend import getPersonInfo, doesWikiPageExist, getCityInfo

def main():
    contextDict = getContext()
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
                if len(tempCityDict) > len(cityDict):
                   cityDict = tempCityDict

        if len(cityDict) <= 1:
            print("No info was found on " + cityName.replace("_", " ") + ", please chose another")

    return cityDict

if __name__ == "__main__":
    main()
