import misc
import re
from collections import Counter

threads = misc.getThreadsAndPostNumbers(1)

joinDates = []

for thread in threads:
	userList = misc.getUserInfo(thread[0])
	for user in userList:
		joinDates.append(user['Join Date'])
c = Counter(joinDates)

topThree = c.most_common(3) # Returns a list of tuples (x_n, y_n)
x = [topThree[i][0] for i in range(3)]
y = [topThree[i][1] for i in range(3)]

barGraph = misc.buildBarGraph(x = x, y = y, title = 'Top three months and years')
misc.dashIt(barGraph, 'Most Common Join Dates', 'Restricted to the First Page of the Misc')
