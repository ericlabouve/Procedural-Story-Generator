# ProceduralStoryGeneration
A research project that explores how the Semantic Web technology SPARQL can be used to enhance procedural story generation systems for NPC applications as applied to CFG story generation. 

## Language Rules:

Rules are formatted as, Key ::= Value, where a Key appears on the LHS and a Value appears on the RHS

Non-terminal nodes start with an upper case letter.

Terminal nodes start with a lower case letter.

All optional elements are surrounded by square brackets [ ].
 - Non-terminal elements inside square brackets will be expanded if its preconditions are satisfied. 
 - Terminal elements inside square brackets will be expanded found in the table. If the terminal element does not exist, it will be replaced with the empty string.
 
Optional element keys precede parentheses ( ) which the contain expansion preconditions. 
 - Preconditions are stated as a boolean expression of terminal variables. 
 - Variables are checked for their existance.

\OR a logical boolean operation for precondition

\AND a logical boolean operation for precondition

Vertical line | is a binary operator that randomly selects an element on either the LHS or the RHS

\OVER is a binary operator that denotes a priority selection, where the element on the left is chosen if it exists, otherwise the right element is chosen

\CHOOSE("identifier", Values...) is a function that will prompt the user to choose how many of the elements will show up in the story.
 - First argument is a string that identifies the scale that the user is evaluating.
 - Subsequent arguments are elements that are chosen at random.
 - If one of the variable elements does not satisfy the preconditions, then it will not be included in the scale.
 - Example: \CHOOSE("Character Detail", [Element1], \<Element2\>) will prompt the user with the following message: "Choose the level of Character Detail between 0 and 2." 

Comments are indicated by a double slash //

## Optional Keys
Using the semantic web query language, Sparql, we can pull information directly from DBPedia. Two broad queries are written for demonstration purposes. The first retrieves person-related information and the second retrieves location-related information. The following keys in the tables are not garunteed to exist because wikipedia pages may be incomplete. Therefor, if a key is used, each key should be surrounded by square brackets.

### Potential Person Properties:
| Key | Meaning |
| :---: | :---: |
| name | Person's English name |
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
| gender | Person's gender expressed as a binary value (male for female) |
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

## Sample Grammar:

```
<Story> ::= <Begining><Middle><End>
<Begining> ::= <Introduce Main Character>
<Middle> ::= <Introduce Goal><Conflict><Resolution><Travel>  
<End> ::= <Obtain Goal>

<Introduce Goal> ::= <name> " has "<Travel Synonymes>" to "<cityName>" in order to "<Find Synonymes>" the "<Object Synonymes>" "<objectname>
    <Travel Synonymes> ::= "traveled" | "ran" | "walked" | "biked" | "flown" | "taken an Uber"
    <Find Synonymes> ::= "find" | "hunt down" | "rediscover" | "catch sight of" | "come across" | "discover" | "encounter" | "locate" | "spot" | "track down" | "uncover"
    <Object Synonymes> ::= "astonishing" | "astounding" | "breathtaking" | "startling" | "stunning"

<Conflict> ::= <Negative Conjunction>", "<Conflict Object Adjectives>" "<Conflict Object>" "<Conflict Action>" "<Conflict Object2><Punctuation>
    <Negative Conjunction> ::= "But" | "However" | "Unfortunately" | "All of a sudden" | "Then" | "Suddenly"
    <Conflict Object Adjectives> ::= "hidden" | "evil" | "ugly" | "smelly" | "vicious" | "aggressive" | "combative" | "contentious" | "destructive" | "intrusive" | "threatening" | "barbaric" | "disturbing" | "militant" | "offensive" | "pugnacious" | "quarrelsome" | "rapacious" | "warlike" | "giant"
    <Conflict Object> ::= "ninjas" | "assassins" | "warriors" | "samurai" | "robots" | "dogs" | "army men" | "zombies" | "vampires" | "assassins" | "monsters" | "birds" | "lions" | "spiders" | "turtles" | "republicans"
    <Conflict Action> ::= "attack" | "charge" | "intrude" | "invade" | "raid" | "strike" | "advance on" | "drive into" | "encroach on" | "mug" | "rush" | "storm"
    <Conflict Object2> ::= <name> | "the city" | "the town" | "the buildings" | "the civilians" 
    <Punctuation> ::= "." | "..." | "!" | "!!" | "!?"

<Resolution> ::= "Then " <name> " <Resolution Action>. ". Afterwards, " <name> <Discover Evidence>
    <Resolution Action> ::= "saves the day" | "wins the battle" | "hides until everyone leaves" | "tricks the foes into leaving" | "runs them out of town" | "defeats them all" | "barely wins the fight"
    <Discover Evidence> ::= <Approach Person><Ask Question><Receive Answer>
    <Approach Person> ::= <Approach Verb>" a "<Approach Noun> " and asks, <Ask Question>" They respond, "
        <Approach Verb> ::= | "approaches" | "walks over to" | "runs over to" | "crawls over to" | 
        <Approach Noun> ::= "local shop owner" | "wounded civilian" | "a defeated enemy"
        <Ask Question> ::= "'Is "<objectname>" in this city?'" | "'Where can I find the " <objectname> "!'"
        <Receive Answer> ::= "No you fool!" | "I wouldn't tell you even if I knew!" | "I have no idea..." | "Try somehwere else?" | "That's been lost for as long as I remember..." | "Oh! Umm... No I don't recall ever seeing such a thing." | "Legend says its gone"
        
<Obtain Goal> ::= "When finding "<objectname>" seemed hopeless, "<name>" "<Goal Action>" and "<name>" finally sees "<objectname>" "<Object Location>"."
    <Goal Action> ::= "trips on a rock" | "is approached by a little girl who points to her left" | "remebers" | "watches the sunset" | "observes the cows in the distance" | "sits on the ground" | "puts on their glasses"
    <Object Location> ::= "in the distance" | "on a hill" | "by the stoplight" | "hanging from a streetlight" | "in a car" | "hanging out of a trash can" | "beside a tree"
```

#### Grammar Modification Scales:

The length of a story can be adjusted using the \\CHOOSE function. As the scale increases, the <Middle> rule expands to include more locations:
  
```
<Travel> ::= \CHOOSE("Travel Extent", <Travel Default>, [Travel North], [Travel NorthWest], [Travel NorthEast], [Travel South], [Travel SouthWest], [Travel SouthEast], [Travel East], [Travel West])
<Travel Default> ::= <Conflict><Resolution>
[Travel North](north) ::= <Travel Transition>" north to " [north]"." <Conflict><Resolution>
[Travel NorthWest](northwest) ::= <Travel Transition>" northwest to " [northwest]"."<Conflict><Resolution>
[Travel NorthEast](northeast) ::= <Travel Transition>" northeast to " [northeast]"."<Conflict><Resolution>
[Travel South](south) ::= <Travel Transition>" south to " [south]"."<Conflict><Resolution>
[Travel SouthWest](southwest) ::= <Travel Transition>" southwest to " [southwest]"."<Conflict><Resolution>
[Travel SouthEast](southeast) ::= <Travel Transition>" southeast to " [southeast]"."<Conflict><Resolution>
[Travel East](east) ::= <Travel Transition>" east to " [east]"."<Conflict><Resolution>
[Travel West](west) ::= <Travel Transition>" west to " [west]"."<Conflict><Resolution>
    <Travel Transition> ::= "To continue the "<Adventure Synonymes>", "<name>" "<Travel Synonymes Present Tense>
    <Adventure Synonymes> ::= "adventure" | "hunt" | "search" | "trip" | "quest"
    <Travel Synonymes Present Tense> ::= "travels" | "runs" | "walks" | "bikes" | "flies" | "takes an Uber"
```
  
Adjust the description of characters. As the scale increases, \<Details\> uses more information from the Person Properties table:
```
<Introduce Main Character> ::= <Name><Details>
    <Name> ::= "There once was a " [nationality] " " <Hypernym> "named" <name> "."
        <Hypernym> ::= [hypernym] \OVER "Person"
<Details> ::= \CHOOSE("Character Detail ", [Birth], [Religion], [School], [Description], [KnownFor], [Awards], [Currently Living], [Family])
    [Birth](birthPlace \OR birthDate \OR parents) ::= <name> " was born " [Birthplace][BirthDate][to <parents>] "." // Birth is condition and requires at least one of the following elements
        [Birthplace](birthplace) ::= " in " [birthPlace]
        [BirthDate](birthDate) ::= " on " [birthDate]
        [Parents](parents) ::= " to " [parents] 
    [Religion](religion)  ::= <Pronoun> " was raised to to believe in " [religion] "."
    [School](school) ::= "When " <name> " came of age, " <Pronoun> studied [fieldOfStudy] at [school] "."
    [Description] ::= "Later in life, " <person> " became a " [description] "."
    [KnownFor](knownFor) ::= "When people come across " <name> " in public, people know " <Pronoun> " for " [knownFor] [NetWorth]
        [Networth](networth) ::= ", which is why " <name> " is now worth $" [networth] 
    [Awards](awards) ::= "Throughout " <name> "'s successful career, " <Pronoun> " received numerous awards such as " [awards] "."
    [Currently Living](residence) ::= "Now, " <name> " lives at " [residence] "."
    [Family](spouse \OR children) ::= <name> "'s family is means the world to " <Pronoun>. <Pronoun>[Spouse][Children] "."
        [Spouse] ::= " loves his spouse " [spouse]
        [Children] ::= " and loves his children " [children]
<Pronoun> ::= // Chosen using <gender> but is replaced with <name> if <gender> is not available.
```


