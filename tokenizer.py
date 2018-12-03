import re

# --------------------- Regular Expression Patterns ---------------------
stringPat = r"\"[a-zA-Z0-9.$!?', ]*\""
elemPat = r'<[a-zA-Z0-9 ]*>'
optElemPat = r'\[[a-zA-Z0-9 ]*\]'
optElemPreconPat = r'\([a-zA-Z0-9\\ ]*\)'
optElemKeyPat = optElemPat + optElemPreconPat
orPat = r'\|'
overPat = r'\\OVER'

# --------------------- Check if String is Regular Expression ---------------------
def isElem(s: str) -> bool:
	''' <ElementName> '''
	return re.search(elemPat, s) is not None

def isOptElem(s: str) -> bool:
	''' [ElementName] '''
	return re.search(optElemPat, s) is not None

def isOptElemKey(s: str) -> bool:
	''' [ElementName](val \OR val2 \AND val3) '''
	return re.search(optElemKeyPat, s) is not None

def isStr(s:str) -> bool:
	'''  "Hello World" '''
	return re.search(stringPat, s) is not None

def isOr(s:str) -> bool:
	''' | '''
	return re.search(orPat, s) is not None

def isOver(s:str) -> bool:
	''' \OVER '''
	return re.search(overPat, s) is not None


# --------------------- Valid Element Tokens ---------------------
class Element:
	''' Elements that appear in angle brackets < >
	'''
	def __init__(self, elemName:str):
		self.elemName = elemName

	def __repr__(self):
		return "<" + self.elemName + ">"

class OptionalElement:
	''' Elements that appear in square brackets [ ] 
		Optional element KEYS have preconditions in parentheses ( )
		If preconditions are not satisfied, then the element is replaced with the empty string.
	'''
	def __init__(self, elemName:str, precondition: str = None):
		self.elemName = elemName
		self.precondition = precondition

	def __repr__(self):
		first = "[" + self.elemName + "]"
		second = "" if self.precondition is None else "(" + self.precondition + ")"
		return first + second

	def isTrue(terminals: dict) -> bool:
		''' Evaluates the optional element as either true or false.
			If precondition exists, then the optional element is a key, else the optional elment is a value
		'''
		pass

class OrElement:
	def __init__(self):
		pass

	def __repr__(self):
		return "|"

class OverElement:
	def __init__(self):
		pass

	def __repr__(self):
		return "\\OVER"

class ChooseElement:
	''' Element that prompts the user to determine how many of the variable arguments should be expanded in a row
		Format: \CHOOSE("Scale Description", variable arguments)
		
		Ex: \CHOOSE("Character Details", <Birth>, <Religion>, <School>)
		In the example above, when the user inputs 2, then two random elements are selected to expand
		
		Ex: \CHOOSE("Character Details", [Birth], [Religion], [School])
		In the example above, elements are optional, so that are first expanded. Say [Birth] does not satisfy
		the preconditions. So, the choose function would be reduced to:
		\CHOOSE("Character Details", [Religion], [School])
	'''
	def __init__(self, scaleName:str, vargs:list):
		self.scaleName = scaleName
		self.vargs = vargs

	def __repr__(self):
		vargsString = ""
		for arg in self.vargs:
			vargsString += repr(arg) + ", "
		# Remove last comma and space
		vargsString = vargsString[0:len(vargsString) - 2]
		return "\\CHOOSE(\"" + self.scaleName + "\", " + vargsString + ")"


class Statement:
	''' A Statement is composed a key and a value. 
		The key is the left hand side of the ::=
		The value is the right hand side of the ::=
	''' 
	def __init__(self, line: str):
		phrases = line.split('::=')
		if len(phrases) != 2:
			raise Exception('Statement:\n\"{}\"\nDoes not contain a key and a value separated by ::=\n'.format(line))
		self.parseKey(phrases[0])
		self.parseValue(phrases[1])

	def __repr__(self):
		return repr(self.key) + " ::= " + repr(self.value)

	def parseKey(self, key: str):
		posPatterns = r"(" + elemPat + "|" + optElemKeyPat + ")"
		match = re.search(posPatterns, key)
		if match is None:
			if re.search(r"(" + optElemPat + ")", key) is not None:
				raise Exception("Conditional Key: \"{}\" requires a condition.\n".format(key))
			else:
				raise Exception('Key: \"{}\" is not properly formatted.\n'.format(key))
		match = match.group(0)
		if isElem(match):
			self.key = parseElem(match)
		elif isOptElemKey(match):
			self.key = parseOptElemKey(match)
		else:
			raise Exception("No pattern found for match\n{}\nIn value:\n{}\n".format(match, value))

	def parseValue(self, value: str):
		self.value = []
		# Check for CHOOSE statement
		if '\\CHOOSE' in value:
			self.value = [parseChoose(value)]		
		else:
			posPatterns = r'(' + stringPat + "|" + elemPat + "|" + optElemPat + "|" + orPat + "|" + overPat + ")"
			for match in re.finditer(posPatterns, value):
				match = match.group(0)
				if isElem(match):
					self.value.append(parseElem(match))
				elif isOptElem(match):
					self.value.append(parseOptElem(match))
				elif isStr(match):
					self.value.append(parseStr(match))
				elif isOr(match):
					self.value.append(parseOr(match))
				elif isOver(match):
					self.value.append(parseOver(match))
				else:
					raise Exception("No pattern found for match\n{}\nIn value:\n{}\n".format(match, value))


# --------------------- Parse String into Token ---------------------
def parseElem(s:str) -> Element:
	# Remove angle brackets
	elemName = re.sub(r'(<|>)', '', s)
	return Element(elemName.strip())

def parseOptElem(s:str) -> OptionalElement:
	elemNameWithBrackets = re.search(optElemPat, s).group(0)
	elemName = re.sub(r'(\[|\])', '', elemNameWithBrackets)
	return OptionalElement(elemName.strip())

def parseOptElemKey(s:str) -> OptionalElement:
	elemNameWithBrackets = re.search(optElemPat, s).group(0)
	elemName = re.sub(r'(\[|\])', '', elemNameWithBrackets)
	elemConditionWithParen = re.search(optElemPreconPat, s).group(0)
	elemCondition = re.sub(r'(\(|\))', '', elemConditionWithParen)
	return OptionalElement(elemName, precondition=elemCondition)

def parseStr(s:str) -> str:
	s = re.search(stringPat, s).group(0)
	s = re.sub(r'\"', '', s)
	return s

def parseOr(s:str):
	return OrElement()

def parseOver(s:str):
	return OverElement()

def parseChoose(s:str) -> ChooseElement:
	'''Parses and return a choose element of the form
		\CHOOSE("Character Detail ", [Element1], [terminal1], <Element2>)
	'''
	matches = s.split(',')
	if len(matches) <= 1:
		raise Exception("CHOOSE statement\n\"{}\"\nDoes not have correst number of arguments".format(s))
	scaleName = parseStr(matches[0])
	vargs = []
	# Evaluate rest of arguments to either Elements or OptionalElements
	for elem in matches[1:]:
		if isElem(elem):
			vargs.append(parseElem(elem))
		elif isOptElem(elem):
			vargs.append(parseOptElem(elem))
		else:
			raise Exception("CHOOSE statement\n\"{}\"\nonly accepts Elements and Optional Elements".format(s))
	return ChooseElement(scaleName, vargs)

def fixFormat(s: str) -> str:
	'''Formats everything according to English grammar rules
		1. Reduces spaces, including before punctuation, Ex: 'Hello w   or ld   ' --> 'Hello world'	
		2. Smoosh apostrophes, commas, periods, ! etc with surrounding text
		3. Capitolize next character after a period and !
	'''
	s = re.sub(r' +', ' ', s).strip()
	s = re.sub(r' \. ', '. ', s)
	s = re.sub(r' ! ', '! ', s)
	s = re.sub(r' , ', ', ', s)
	s = re.sub(r' \? ', '? ', s)
	s = re.sub(r" '", "'", s)

	def find_all(a_str, sub):
		start = 0
		idxs = []
		while True:
			start = a_str.find(sub, start)
			if start == -1: 
				return idxs
			idxs += [start]
			start += len(sub)
	def capitalize_nth(s, n):
		return ''.join([s[:n], s[n].upper(), s[n + 1:]])
	def capitalizeAfter(s, ch):
		idxs = find_all(s, ch)
		for idx in idxs:
			firstLetter = idx + 1
			secondLetter = idx + 2
			if firstLetter < len(s) and firstLetter is ' ' and secondLetter is not ' ':

				s = capitalize_nth(s, secondLetter)
		return s
	s = capitalizeAfter(s, '.')
	s = capitalizeAfter(s, '!')
	s = capitalizeAfter(s, '?')
	return s


if __name__ == "__main__":
	s = "There once was a Person named Barack Obama . Barack Obama was born in Kapiolani Medical Center for Women and Children on 1961-8-4 to Ann Dunham . They was raised to to believe in Protestantism . When Barack Obama came of age, they studied at Harvard Law School . Later in life, Barack Obama became a 44th President of the United States . Throughout Barack Obama 's successful career, they received numerous awards such as Nobel Peace Prize . Now, Barack Obama lives at White House . Barack Obama 's family means the world to them They love their spouse Michelle Obama and love their children Malia . Barack Obama ran to San Francisco in order to come across the astonishing diamond But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs north to (Marin County) . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs northwest to Marin Headlands . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs northeast to (Contra Costa County) . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs south to (San Mateo County) . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs southeast to (Alameda County) . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs east to (Alameda County) . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! To continue the hunt , Barack Obama runs west to Pacific Ocean . But , aggressive warriors encroach on the civilians . Then Barack Obama hides until everyone leaves . Afterwards, Barack Obama approaches a a defeated enemy and asks, diamond They respond, diamond I wouldn't tell you even if I knew! When finding diamond seemed hopeless, Barack Obama is approached by a little girl who points to her left and Barack Obama finally sees diamond in a car ."
	#print(s)
	print(fixFormat(s))


if __name__ == "__main0__":
	with open('sampleGrammar1.txt', 'r') as myfile:
		grammar = re.sub(r' +', ' ', myfile.read())
	#grammar = '<Travel> ::= \\CHOOSE("Travel Extent", <Travel Default>, [Travel North])\n'
	lines = grammar.split('\n')
	statements = []
	for line in lines:
		line = line.strip()
		if len(line) > 0:
			statements.append(Statement(line))
	for s in statements:
		print(s)
