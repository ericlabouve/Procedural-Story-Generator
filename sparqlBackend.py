from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import json, os, requests

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Pretty print json: print(json.dumps(jsonObj, indent=4, sort_keys=True))

def printJson(jsonVal):
	print (json.dumps(jsonVal, indent=2, sort_keys=True))

def isURI(uri: str) -> bool:
	return "http://" in uri

def dereferenceURI(uri: str) -> str:
	if isURI(uri):
		sparql.setQuery("""
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			SELECT DISTINCT ?label
		    WHERE { 
		    	<URI> rdfs:label ?label .
		    	FILTER (lang(?label) = 'en')
		    }
		""".replace("URI", uri))
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		if len(results["results"]["bindings"]) == 0:
			return uri.split('/')[-1]
		else:
			return results["results"]["bindings"][0]["label"]["value"]
	else:
		return uri

def simplify(sparqlResults, queryNames) -> defaultdict:
	"""
	Simplifies the return format of the sparql query by dereferencing all URIs
	and converting the object into a dictionary.
	sparqlResults - The results of a sparql query converted to Json format.
	returns a dictionary with key = table's column and value = list table elements 
	"""
	# Dictionary to hold temporary uri results
	d_uris = defaultdict(list)
	# Simplify return format - Loop through each row item
	for result in sparqlResults["results"]["bindings"]:
		# Loop through each column header
	    for key in sparqlResults["head"]["vars"]:
	    	# If there exists an element in this column and we have not seen this element
	    	if key in result and result[key]["value"] not in d_uris[key]:
	    		d_uris[key].append(result[key]["value"])
	# Dereference URIs
	d_values = defaultdict(list)
	for key, uriArr in d_uris.items():
		for uri in uriArr:
			d_values[key].append(dereferenceURI(uri))
	for key in queryNames:
		if key not in d_values:
			d_values[key] = ""
	return d_values

def getPersonInfo(person: str) -> defaultdict:

	queryNames = ["personName" ,"birthPlace","birthDate" ,"description",
		"school", "award", "religion", "residence", "spouse",
       		"children", "parents", "hypernym", "sex", "networth",
		"fieldOfStudy", "knownFor", "nationality"]

	sparql.setQuery("""
		PREFIX dbo: <http://dbpedia.org/ontology/>
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		PREFIX res: <http://dbpedia.org/resource/>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX purl: <http://purl.org/dc/terms/>
		PREFIX dbpedia2: <http://dbpedia.org/property/>

	    SELECT DISTINCT ?""" + " ?".join(queryNames) + """ 
            WHERE { 
			OPTIONAL { res:PERSON foaf:name ?personName . }
			OPTIONAL { res:PERSON dbo:birthPlace ?birthPlace . }
			OPTIONAL { res:PERSON dbo:birthDate ?birthDate . }
			OPTIONAL { res:PERSON purl:description ?description . }
			OPTIONAL { res:PERSON dbo:almaMater ?school . }
			OPTIONAL { res:PERSON dbo:award ?award . }
			OPTIONAL { res:PERSON dbo:religion ?religion . }
			OPTIONAL { res:PERSON dbo:residence ?residence . }
			OPTIONAL { res:PERSON dbo:spouse ?spouse . }
			OPTIONAL { res:PERSON dbpedia2:children ?children . }
			OPTIONAL { res:PERSON dbpedia2:parents ?parents . }
			OPTIONAL { res:PERSON purl:hypernym ?hypernym . }
			OPTIONAL { res:PERSON foaf:gender ?sex . }
			OPTIONAL { res:PERSON dbo:networth ?networth . }
			OPTIONAL { res:PERSON dbo:field ?fieldOfStudy . }
			OPTIONAL { res:PERSON dbo:knownFor ?knownFor . }
			OPTIONAL { res:PERSON dbpedia2:nationality ?nationality . }
	    }""".replace("PERSON", person))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return simplify(results, queryNames)


def getCityInfo(city: str) -> defaultdict:
	queryNames = ["cityName", "country", "nickname", "isPartOf", 
			"leaderName", "leaderTitle", "populationTotal", 
			"east", "north", "northeast", "northwest", "south", 
			"southeast", "southwest", "west"] 

	# You cannot use a PREFIX if the value after the colon has a comma, so the full URI is used here
	queryStr = """
		PREFIX dbo: <http://dbpedia.org/ontology/>
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX dbpedia2: <http://dbpedia.org/property/>

		SELECT DISTINCT ?""" + " ?".join(queryNames) + """ 
                WHERE {
			OPTIONAL { <http://dbpedia.org/resource/CITY> rdfs:label ?cityName . FILTER (lang(?cityName) = 'en') . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbo:country ?country . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> foaf:nick ?nickname . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbo:isPartOf ?isPartOf . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbo:leaderName ?leaderName . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbo:leaderTitle ?leaderTitle . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbo:populationTotal ?populationTotal . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:east ?east . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:north ?north . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:northeast ?northeast . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:northwest ?northwest . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:south ?south . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:southeast ?southeast . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:southwest ?southwest . }
			OPTIONAL { <http://dbpedia.org/resource/CITY> dbpedia2:west ?west . }
		}""".replace("CITY", city)
	sparql.setQuery(queryStr)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return simplify(results, queryNames)


def doesWikiPageExist(page: str) -> bool:
	wikiBaseUrl = 'https://en.wikipedia.org/wiki/'
	request = requests.get(wikiBaseUrl + page)
	if request.status_code == 200:
	    return True
	else:
	    return False

def lenCityDict(cityDict: dict) -> int:
	numValidTraits = 0
	for trait in cityDict:
            if cityDict[trait] is not "":
                numValidTraits += 1
	return numValidTraits


if __name__ == "__main__":
	cityName = input("Enter a well known city: ").title().replace(" ", "_")
	stateName = input("Is this city located in America?\nIf so, enter the state/province. Else press enter: ").title().replace(" ", "_")
	page1 = cityName + ",_" + stateName
	page2 = cityName
	# Get DBPedia info if wiki page exists. 
	# Need to query both pages bec wikipedia has inconsistent naming conventions
	print("Retrieving information, one moment...")
	cityDict = defaultdict()
	for page in [page1, page2]:
		if doesWikiPageExist(page):
			tempCityDict = getCityInfo(page)
			if lenCityDict(tempCityDict) > lenCityDict(cityDict):
				cityDict = tempCityDict

	if len(cityDict) > 1:
		for key, value in cityDict.items():
			print(key + " = " + str(value))
	else:
		print("No info was found on " + cityName.replace("_", " "))



if __name__ == "__main__":
	# Capitolize first letter of each word and make cammel case
	personName = input("Enter a famous person's name: ").title().replace(" ", "_")
	print("Retrieving information, one moment...")
	d = getPersonInfo(personName)
	if len(d) > 1:
		for key, value in d.items():
			print(key + " = " + str(value))
	else:
		print("No info was found on " + personName.replace("_", " "))


