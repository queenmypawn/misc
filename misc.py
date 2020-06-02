from collections import Counter
from lxml import html
import requests
import stopwords as sw
import re

# Create an object 'Misc' with the following properties:

bodybuildingURL = 'https://forum.bodybuilding.com/'
miscURL = 'https://forum.bodybuilding.com/forumdisplay.php?f=19'
postListXPath = '//blockquote[@class="postcontent restore "]/text()'
threadListXPath = '//a[@class="title"]/@href'
numOfPostsPerPageXPath = '//td[@class="othercol td-reply"]/text()'
endOfNewPost = '\r\n\t\t\t\t\t\t'

def getDateTime():
	# datetime object containing current date and time
	now = datetime.now()
	
	# Time
	dt_string = now.strftime("%m/%d/%Y %I:%M %p")

	return dt_string

def getTree(webpage):
	page = requests.get(webpage)
	return html.fromstring(page.content)

def getXPathContent(webpage, xpath):
	page = requests.get(webpage)
	tree = html.fromstring(page.content)
	return tree.xpath(xpath)

def itemsOnly(listToAppendTo, originalList):
	for i in range(len(originalList)):
		listToAppendTo.append(originalList[i])

# Takes the xpath of the thread and delivers the posts without the returns, newlines and tabs.
def removeFormatting(lines):
	endOfPostIndexes = [0]
	formattedPostList = []
	for i in range(len(lines)):
		# Track end of posts
		if lines[i].endswith('\r\n\t\t\t\t\t\t'):
			endOfPostIndexes.append(i)
	# Add posts to formatted post list
	currentIndex = 0
	string = []
	for i in range(len(lines)):
		string.append(lines[i])
		# Create and append the post to the 'cooked' post list.
		if i != 0 and i in endOfPostIndexes:
			formattedPostList.append(''.join(string))
			string = []
	# Remove whitespace
	for i in range(len(formattedPostList)):
		formattedPostList = [' '.join(post.split()) for post in formattedPostList]
	# Add images to post list
	for i in range(len(formattedPostList)):
		if len(formattedPostList[i]) == 0:
			formattedPostList[i] = '[image(s)]'
	return formattedPostList

def printPosts(postList, pageNumber = 1):
	for i in range(len(postList)):
		'''if postList[i] == None:
			continue'''
		print(f'Post {((pageNumber - 1)*30) + (i + 1)}: {postList[i]}')

def getPostContent(threadPage):
	posts = []
	postContent = []
	xpathContent = getXPathContent(threadPage, postListXPath)
	postContent = removeFormatting(xpathContent)
	posts.append(itemsOnly(posts, postContent))
	for item in posts:
		if item == None:
			posts.remove(item)
	return posts

def getThreadsAndPostNumbers(pages):
	# Threads
	numOfPosts = []
	threadsWithPostNumbers = []
	firstPage = True
	for i in range(1, pages + 1):
		listOfThreads = []
		url_String = f'{miscURL}&page={i}'
		tree = getTree(url_String)
		threadURL = tree.xpath(threadListXPath)
		listOfThreads.append(threadURL)
		# Their post numbers
		numOfPosts = tree.xpath(numOfPostsPerPageXPath)
		numOfPosts = [''.join(item.split()) for item in numOfPosts]
		# Form the tuples and append them
		if firstPage:
			for i in range(31): # The number of threads per page including stickies.
				threadsWithPostNumbers.append((listOfThreads[0][i], numOfPosts[i]))
		else:
			for i in range(25): # The number of threads per page not including stickies.
				threadsWithPostNumbers.append((listOfThreads[0][i], numOfPosts[i]))
		firstPage = False
	return threadsWithPostNumbers

def searchPhraseInThread(thread, page_limit, **kwargs):
	count = 0
	for i in range(page_limit):
		interestingURL = f'{bodybuildingURL}{thread}&page={i}'
		values = [item for item in kwargs.values()][0]
		for value in values:
			postContent = getPostContent(interestingURL)
			for post in postContent:
				if value in post: # Needs a checker for how many pages in thread.
					count += 1
	return count

