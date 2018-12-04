# ProceduralStoryGeneration
A research project that explores how the Semantic Web technology SPARQL can be used to enhance procedural story generation systems for NPC applications as applied to CFG story generation. 

We hypothesize that the semantic web can be used to generate more in-depth text stories by extrapolating information from user input.

## Language Rules:

Rules are formatted as, Key ::= Value, where a Key appears on the LHS and a Value appears on the RHS

Non-terminal nodes start with an upper case letter and are surrounded by angle brackets < >.

Terminal nodes start with a lower case letter.

If a node is optional, such as in the case of Sparql values, then it is surrounded by square brackets [ ] instead of angle brackets.
 - Non-terminal nodes inside square brackets will be expanded if its preconditions are satisfied. 
 - Terminal nodes inside square brackets will be expanded found in the table. If the terminal node does not exist, it will be replaced with the empty string.
 
Optional node keys precede parentheses ( ) which the contain expansion preconditions. 
 - Preconditions are stated as a boolean expression of terminal variables. 
 - Variables are checked for their existance.

\OR a logical boolean operation for precondition

\AND a logical boolean operation for precondition

Vertical line | is a binary operator that randomly selects a node on either the LHS or the RHS

\OVER is a binary operator that denotes a priority selection, where the node on the left is chosen if it exists, otherwise the right node is chosen

\CHOOSE("identifier", Values...) is a function that will prompt the user to choose how many of the nodes will show up in the story.
 - First argument is a string that identifies the scale that the user is evaluating.
 - Subsequent arguments are nodes that are chosen at random.
 - If one of the variable nodes does not satisfy the preconditions, then it will not be included in the scale.
 - Example: \CHOOSE("Character Detail", [Element1], \<Element2\>) will prompt the user with the following message: "Choose the level of Character Detail between 0 and 2." 

Comments are indicated by a double slash //

## Optional Keys
Using the semantic web query language, Sparql, we can pull information directly from DBPedia. Two broad queries are written for demonstration purposes. The first retrieves person-related information and the second retrieves location-related information. The following keys in the tables are not garunteed to exist because wikipedia pages may be incomplete. Therefor, if a key is used, each key should be surrounded by square brackets.

### Potential Person Properties:
| Key | Meaning |
| :---: | :---: |
| personName | Person's English |
| birthPlace | City where person was born |
| birthDate | Numerical birth date |
| description | Short description of person's career |
| school | Where the person when to university |
| award | Award(s) that the person has been awarded |
| religion | Person's active religion |
| residence | Where the person currently lives |
| spouse | Who person is married to |
| children | Either a list of children names or how many children person has |
| parents | List of the names of person's parents |
| hypernym | What type of person, such as an Actor. |
| sex | Person's sex expressed as male for female |
| networth | Net worth expressed in scientific notation |
| fieldOfStudy | Field of study |
| knownFor | Short description of what the person is known for |
| nationality | Person's nationality |

### Potential City Properties:
| Key | Meaning |
| :---: | :---: |
| cityName | City's English name | 
| country | Country where city is located |  
| nickname | Nicknames that the city goes by | 
| isPartOf| Further description of the city | 
| leaderName | Current political leader(s) |  
| leaderTitle| Political leader's title(s) | 
| populationTotal| Population count | 
| east | Cities or land masses located directly east of the city | 
| north | Cities or land masses located directly nort of the city | 
| northeast | Cities or land masses located directly northeast of the city |   
| northwest | Cities or land masses located directly northwest of the city | 
| south | Cities or land masses located directly south of the city | 
| southeast | Cities or land masses located directly southeast of the city |  
| southwest | Cities or land masses located directly southwest of the city | 
| west | Cities or land masses located directly west of the city | 

### Potential Object Properties:
This is an area of future work. It is hard to identify general objects on Wikipedia. For example, there is not page for Panda, instead there is a page for Giant Panda. However, an average person would not think to search Giant Panda instead of Panda. The area of research would be to guess a related Wikipedia page using a vague user input.

| Key | Meaning |
| :---: | :---: |
| objectname | User defined object that the character is searching for in the story |

## Sample Grammars:

The following grammar demonstrates the use of optional nodes and the \\OVER operator:

```
<Root> ::= [Name][Details]<Action>
[Name](personName) ::= [personName]
[Details](sex \AND description) ::= ", the " [sex] " " [description]","
<Action> ::= " suddenly woke from a nightmare about his "<Dream> "."
<Dream> ::= [Options] \OVER <Default>
[Options](birthPlace \OR school) ::= [BirthPlace] | [School]
[BirthPlace](birthPlace) ::= "troubling childhood in " [birthPlace]
[School](school) ::= "thesis defence at " [school]
<Default> ::= "secret affair"
```

Here are two sample outputs when a user inputs "Napolean" and "Barack Obama" for the personName:

“Napoleon, the male French monarch, military andpolitical leader, suddenly woke from a nightmareabout his troubling childhood in Corsica.”

“Barack Obama, the male 44th President of theUnited States, suddenly woke from a nightmareabout his thesis defence at Harvard Law School.”

The following grammar demonstrates the use of the \\CHOOSE function. This function is used to adjust the length of a story. The tool will prompt the user to enter the number of nodes to expand and will proceed to expand the corresponding number of nodes:

```
[Root](cityName) ::= "To explore the areas around " [cityName] ", our character " <Travel> "went to bed."
<Travel> ::= \CHOOSE("Travel", <Default>, [North], [South], [East], [West])
<Default> ::= "looked at a map, then "
[North](north) ::= <Moved>" north to " [north]", then "
[South](south) ::=<Moved>" south to " [south]", then "
[East](east) ::=<Moved>" east to " [east]", then "
[West](west) ::=<Moved>" west to " [west]", then "
<Moved> ::= "traveled" | "ran"| "walked" | "biked"| "flew" | "took an Uber"
```

Here are two sample outputs when a user inputs "San Jose" for the cityName and "2" for the \\CHOOSE function:

“To explore the area around San Jose, ourcharacter biked north to Milpitas, California, thentook an Uber east to Mount Hamilton, California,then went to bed.”

“To explore the area around San Jose, ourcharacter looked at a map, then flew south toMorgan Hill, California, then went to bed.”

## User Study

The Google form that was used for the user study is located bellow. Studies were done in classroom like environemnt. Results are still pending.

https://docs.google.com/forms/d/e/1FAIpQLSfEeroEJ7WMMVLkenmuT_1CoZykhxAPVCB-COpVkz3AuMxjAw/viewform?usp=sf_link
