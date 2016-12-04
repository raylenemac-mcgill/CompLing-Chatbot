README

Creators:
Raylene MacDonald
Imogen Holland
Shubha Murthy

Penny is a chatbot created for our final project for LING 550 (Computational Linguistics) in Fall 2016. Our chatbot's specialty is making puns and other types of jokes related to the user’s previous input. For instance, if you ask Penny to “tell me a joke about llamas”, she might respond with a pun about alpacas (alpacas and llamas are “semantically similar”). Penny uses a sister program called Nickel, which can organically create jokes of a certain template. For instance, if you say “I went to the bazaar today”, she might reply “What to do you call a strange market? A bizarre bazaar!” These types of jokes are created using both semantic and phonetic similarity, as well as Pydictionary, a synonym finder.
Currently Penny only provides a command-line interface. In the future we might develop a GUI.

DEPENDENCIES
To get Penny installed and running, you will need to install Python 3, NLTK and Pydictionary.
Install Python 3: http://www.python.org/downloads/
pip install PyDictionary
pip install -U nltk (make sure CMUDict is included in your installation)


To supress the BeautifulSoup warning, follow the path specified in the warning
(on Windows: \AppData\Local\Programs\Python\Python35-32\lib\site-packages\bs4\__init__.py:181 )
and comment out the warning. We are currently searching for a better solution to this problem.
