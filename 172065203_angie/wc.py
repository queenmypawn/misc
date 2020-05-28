from collections import Counter
from lxml import html
import requests
from datetime import datetime
import stopwords as sw

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%m/%d/%Y %I:%M %p")

# Thread: "Angie Varona is at her peak right now IMO"
webpage = 'https://forum.bodybuilding.com/showthread.php?t=172062503'
page = requests.get(webpage)
tree = html.fromstring(page.content)

pageString = tree.xpath('//a[@class="popupctrl"]/text()')
title = tree.xpath('//a[@title="Reload this Page"]/text()')[0]
numPages = pageString[-1][-1]

wordList = []


for i in range(1, int(numPages) + 1):
	print(f'On page {i}')
	page = requests.get(f'https://forum.bodybuilding.com/showthread.php?t=172062503=&page={i}')
	tree = html.fromstring(page.content)
	posts = tree.xpath('//blockquote[@class="postcontent restore "]/text()')
	wordList.append(''.join(posts).split())

wordList = [word for sublist in wordList for word in sublist if word not in sw.stopWords] # Change it to a class and use a get function.
popularWords = list(Counter(wordList).most_common())

