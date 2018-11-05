from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import json, os

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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
		return results["results"]["bindings"][0]["label"]["value"]
	else:
		return uri

def simplify(sparqlResults) -> defaultdict:
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
	return d_values

def getPersonInfo(person: str) -> defaultdict:
	sparql.setQuery("""
		PREFIX dbo: <http://dbpedia.org/ontology/>
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		PREFIX res: <http://dbpedia.org/resource/>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX purl: <http://purl.org/dc/terms/>
		PREFIX dbpedia2: <http://dbpedia.org/property/>

	    SELECT DISTINCT ?name ?birthPlace ?birthDate ?description 
	    				?school ?award ?religion ?residence ?spouse 
	    				?children ?parents ?hypernym ?gender ?networth 
	    				?fieldOfStudy ?knownFor ?nationality
	    WHERE { 
			OPTIONAL { res:PERSON foaf:name ?name . }
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
			OPTIONAL { res:PERSON foaf:gender ?gender . }
			OPTIONAL { res:PERSON dbo:networth ?networth . }
			OPTIONAL { res:PERSON dbo:field ?fieldOfStudy . }
			OPTIONAL { res:PERSON dbo:knownFor ?knownFor . }
			OPTIONAL { res:PERSON dbpedia2:nationality ?nationality . }
	    }""".replace("PERSON", person))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return simplify(results)

if __name__ == "__main__":
	personName = input("Enter a famous person's name: ")
	# Capitolize first letter of each word and make cammel case
	personName = personName.title().replace(" ", "_")
	print("Retrieving information, one moment...")
	d = getPersonInfo(personName)
	for key, value in d.items():
		print(key + " = " + str(value))


