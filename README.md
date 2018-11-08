# ProceduralStoryGeneration
A research project that explores how the Semantic Web technology SPARQL can be used to enhance procedural story generation systems for NPC applications.


## Initial Grammar:

```
NOTE: Square brackets denote optional elements, * indicates a clean star,  and // indates a comment
<Story> ::= <Begining><Middle><End>
<Begining> ::= <Introduce Main Character><Introduce Goal>  
<Middle> ::= <Travel to Location><Conflict><Resolution>  
<End> ::= <Obtain Goal>
```

#### Grammar Modification Scales:

Adjust the length of the story. As the scale increases, the <Middle> rule expands to include more locations:
  
```
<Middle> ::= [<Travel to Location><Conflict>]*
```
  
Adjust the description of characters. As the scale increases, \<Details\> uses more information from the Person Properties table:
```
<Introduce Main Character> ::= <Name><Details>
    <Name> ::= There once was a <Hypernym> named <name>.
        <Hypernym> ::= <hypernym> | Person
<Details> ::= [<Birth>][<Religion>][<School>][<Description>][<KnownFor>][<Awards>][<Currently Living>][<Family>]
    <Birth> ::= <name> was born in <birthPlace> on <birthDate> [to <parents>].
    <Religion>  ::= <Pronoun> was raised to to believe in <religion>.
    <School> ::= When <name> came of age, <Pronoun> studied [<fieldOfStudy> | ""] at <school>.
    <Description> ::= Later in life, <person> became a <description>.
    <KnownFor> ::= When people come across <name> in public, people know <Pronoun> for <knownFor> [, which is why <name> is now worth $<networth>]
    <Awards> ::= Throughout <Pronoun> successful career, <name> received numerous awards such as <awards>.
    <Currently Living> ::= Now, <name> lives at <residence>.
    <Family> ::= <name>'s family is means the world to <Pronoun>. <Pronoun> loves his spouse <spouse> [and his children <children>].
<Pronoun> ::= // Chosen using <gender> but is replaced with <name> if <gender> is not available.
```

## Potential Person Properties:
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

## Potential City Properties:
| Key | Meaning |
| :---: | :---: |
| name | City's English name | 
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

