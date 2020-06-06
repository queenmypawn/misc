from collections import Counter
from lxml import html as html_lxml
import requests
import stopwords as sw
import re
from plotly import graph_objects as go
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

# Create an object 'Misc' with the following properties:

bbURL = 'https://forum.bodybuilding.com/'
miscURL = 'https://forum.bodybuilding.com/forumdisplay.php?f=19/'
postListXPath = '//blockquote[@class="postcontent restore "]/text()'
threadListXPath = '//a[@class="title"]/@href'
numOfPostsPerPageXPath = '//td[@class="othercol td-reply"]/text()'
userNameXPath = '//a[@class="username popupctrl"]/strong/text()'
userInfoXPath = '//dl[@class="userinfo_extra"]/dt/text()'
repPowerXPath = '//dl[@class="userinfo_extra"]/dt/span/text()'
endOfNewPost = '\r\n\t\t\t\t\t\t'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

'''def kwargs_unpacker():'''

def getDateTime():
	# datetime object containing current date and time
	now = datetime.now()
	
	# Time
	dt_string = now.strftime("%m/%d/%Y %I:%M %p")

	return dt_string

def getTree(webpage):
	page = requests.get(webpage)
	return html_lxml.fromstring(page.content)

def getXPathContent(webpage, xpath):
	page = requests.get(webpage)
	tree = html_lxml.fromstring(page.content)
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

# Returns a list of 2-tuples with threads and post numbers.
def getThreadsAndPostNumbers(threads = 25, pages = 1, noStickies = False): # Add post min., post max. requirement
	# Threads
	if not isinstance(threads, int) or threads > 25:
		raise Exception("You broke the program! Negged.")
	numOfPosts = []
	threadsWithPostNumbers = []
	firstPage = True
	for i in range(1, pages + 1):
		listOfThreads = []
		url_String = f'{miscURL}&page={i}'
		tree = getTree(url_String)
		threadURL = tree.xpath(threadListXPath)
		listOfThreads.append(threadURL)
		print(f'In page {i}')
		# Their post numbers
		numOfPosts = tree.xpath(numOfPostsPerPageXPath)
		numOfPosts = [''.join(item.split()) for item in numOfPosts]
		# Form the tuples and append them
		if firstPage:
			if noStickies == True:
				for i in range(6, threads + 6): # Assumes 6 stickies. Sticky counter can be built, though.
					threadsWithPostNumbers.append((f'{bbURL}{listOfThreads[0][i]}', numOfPosts[i]))				
			else:			
				for i in range(threads + 6): # The number of threads per page including stickies.
					threadsWithPostNumbers.append((f'{bbURL}{listOfThreads[0][i]}', numOfPosts[i]))		
		else:			
			for i in range(threads): # The number of threads per page not including stickies.
				threadsWithPostNumbers.append((f'{bbURL}{listOfThreads[0][i]}', numOfPosts[i]))
		
		firstPage = False
		if i == pages: # debugging purposes
			print("End of program")
	return threadsWithPostNumbers

def searchPhraseInThread(thread, page_limit, *args):
	count = 0
	for i in range(page_limit):
		interestingURL = f'{bodybuildingURL}{thread}&page={i}'
		values = [item for item in args]
		for value in values:
			postContent = getPostContent(interestingURL)
			for post in postContent:
				if value in post: # Needs a checker for how many pages in thread.
					count += 1
	return count

# Returns a list of dictionary of users with username, join date, posts, rep power as keys.
def getUserInfo(webpage):
	tree = getTree(webpage)
	userList = tree.xpath(userNameXPath)
	unFormattedUserInfo = tree.xpath(userInfoXPath)
	repPowerInfo = tree.xpath(repPowerXPath)
	userInfo = [unFormattedUserInfo[i] for i in range(len(unFormattedUserInfo))
		if unFormattedUserInfo[i] != ' ' and not unFormattedUserInfo[i].startswith('Location')
		and not unFormattedUserInfo[i].startswith('Age')]
	allUserData = []
	j = 0
	for i in range(len(userList)):
		userData = dict()
		userData['Username'] = userList[i]
		userInfo[j] = userInfo[j].replace('Join Date: ', '')
		userData['Join Date'] = userInfo[j]
		# Age to be added soon...but not all users have an age.
		# Location to be added soon...but not all users have a location.
		userInfo[j + 1] = userInfo[j + 1].replace('Posts: ', '')
		userData['Posts'] = userInfo[j + 1]
		userInfo[j + 2] = repPowerInfo[i].replace('Rep Power: ', '')
		userData['Rep Power'] = repPowerInfo[i]
		j += 3
		allUserData.append(userData)
	return allUserData

def buildBarGraph(x = [], y = [], title = '', time = lambda:getDateTime()):
	keys = x
	values = y

	graph = go.Figure([go.Bar(
		x = x,
		y = y,
		)])

	# Prettifying the bar chart
	graph.update_layout(
	    title = f'{title}, {time()}',
	    title_x = 0.5, # Centralizing the title
	    )
	return graph

def buildScatter(x = [], y = [], title = '', time = lambda:getDateTime(), text=''):
	keys = x
	values = y

	graph = go.Figure([go.Scatter(
		x = x,
		y = y,
		mode = 'markers+text',
		text = text,
		textposition = 'bottom center'
		)])

	# Prettifying the bar chart
	graph.update_layout(
	    title = f'{title}, {time()}',
	    title_x = 0.5, # Centralizing the title
	    )
	return graph

def dashIt(graph = None, graph2 = None, pageTitle = '', pageDesc = ''): # **kwargs): <--- Add multiple graphs.

	# graphs = [graph for graph in kwargs.values()][0]

	app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

	app.layout = html.Div([

        html.H1(pageTitle),
        html.Div(pageDesc),
		html.Div([
	        html.Div([
	            dcc.Graph(id='Chart {i}', figure = graph)
	        ], className='nine columns'),
		]),

	])
	app.run_server()
