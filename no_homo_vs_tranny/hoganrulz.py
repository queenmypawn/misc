from collections import Counter
from lxml import html
import requests
from datetime import datetime
import stopwords as sw

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%m/%d/%Y %I:%M %p")

# Threads: All on first page
mainpage = 'https://forum.bodybuilding.com/forumdisplay.php?f=19'
page = requests.get(mainpage)
tree = html.fromstring(page.content)

listOfThreads = tree.xpath('//a[@class="title"]/@href') # Only unread threads
numOfPosts = tree.xpath('//td[@class="othercol td-reply"]/text()')
numOfPosts = [''.join(item.split()) for item in numOfPosts] # Remove \r, \n, \t characters.

# Remove comma from numbers
numOfPosts = [postNum.replace(',', '') for postNum in numOfPosts]

print(numOfPosts)

# Skip any threads longer than 10 pages or it will take forever
listOfThreads = [listOfThreads[i] for i in range(len(listOfThreads)) if numOfPosts[i] != '-' and int(numOfPosts[i]) <= 9000]

wordList = []
phrase1 = 'no homo'
phrase2 = 'No homo'
phrase3 = 'no Homo'
phrase4 = 'NO HOMO'

phrase5 = 'tranny'
phrase6 = 'Tranny'
phrase7 = 'TRANNY'

p1count = 0
p2count = 0
# Visit a thread
count = 0
for thread in listOfThreads:
	count += 1
	threadPage = f'https://forum.bodybuilding.com/{thread}'
	print(f'Currently in thread: {threadPage}')

	page = requests.get(threadPage)
	threadTree = html.fromstring(page.content)

	# Get the number of pages so we know how many times to iterate.
	pageString = ''.join(threadTree.xpath('//div[@class="postpagestats"]/text()')).split()[-1]
	numPages = int(pageString)//30 + 1
	for i in range(1, int(numPages) + 1):
		print(f'On page {i} of thread {count} of {len(listOfThreads)}')
		page = requests.get(f'https://forum.bodybuilding.com/{thread}&page={i}')
		tree = html.fromstring(page.content)
		posts = tree.xpath('//blockquote[@class="postcontent restore "]/text()')
		wordList.append(''.join(posts).split())

newWordList = []

# Convert the wordlist to something readable
for i in range(len(wordList)):
	newWordList.append(' '.join(wordList[i]))

# Count phrases in the page
for i in range(len(newWordList)):
	p1count += newWordList[i].count(phrase1)
	p1count += newWordList[i].count(phrase2)
	p1count += newWordList[i].count(phrase3)
	p1count += newWordList[i].count(phrase4)

	p2count += newWordList[i].count(phrase5)
	p2count += newWordList[i].count(phrase6)
	p2count += newWordList[i].count(phrase7)

#wordList = [word for sublist in wordList for word in sublist if word not in sw.stopWords] # Change it to a class and use a get function.
#popularWords = list(Counter(wordList).most_common())
#print(popularWords)

print(f'No Homo count: {p1count}')
print(f'Tranny count: {p2count}')
