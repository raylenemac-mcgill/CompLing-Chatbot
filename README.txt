README

Creators:
Raylene MacDonald
Imogen Holland
Shubha Murthy

Penny is a chatbot created for our final project for LING 550 (Computational Linguistics) in Fall 2016. Our chatbot's specialty is making puns and other types of jokes related to the user’s previous input. For instance, if you ask Penny to “tell me a joke about llamas”, she might respond with a pun about alpacas (alpacas and llamas are “semantically similar”). Penny uses a sister program called Nickel, which can organically create jokes of a certain template. For instance, if you say “I went to the bazaar today”, she might reply “What to do you call a strange market? A bizarre bazaar!” These types of jokes are created using both semantic and phonetic similarity, as well as Pydictionary, a synonym finder.
Currently Penny only provides a command-line interface. In the future we might develop a GUI.

DEPENDENCIES
To get Penny installed and running, you will need to install Python 3, NLTK and PyDictionary.
Install Python 3: http://www.python.org/downloads/
pip install PyDictionary
pip install -U nltk (make sure CMUDict is included in your installation)


How to suppress the BeautifulSoup4 warning:
Run Penny2.py. Enter the word “clean”.
When a warning appears, it should include a link to the python file (__init__.py) that must be edited in order to remove the warning. Click this link. If this link does not appear, it can also be found in Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5/site-packages/bs4 (on a Mac computer running Python 3).
(on Windows: \AppData\Local\Programs\Python\Python35-32\lib\site-packages\bs4\__init__.py:181 )
Go to the line “warnings.warn(self.NO_PARSER_SPECIFIED_WARNING % dict(“, which should be line 177. Comment out that line and the next four (until “markup_type=markup_type))”).

We are currently searching for a better solution to this problem.