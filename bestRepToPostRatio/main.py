import misc
from collections import Counter # Belongs in misc.py

# Function to sort the list of tuples by its second item 
def Sort_Tuple(tup):  
      
    # getting length of list of tuples 
    lst = len(tup)  
    for i in range(0, lst):  
        # Bubble Sort
        for j in range(0, lst-i-1):  
            if (tup[j][1] > tup[j + 1][1]):  
                temp = tup[j]  
                tup[j]= tup[j + 1]  
                tup[j + 1]= temp  
    return tup  

threads = misc.getThreadsAndPostNumbers(
	threads = 25,
	pages = 10,
	noStickies = True
	)

users = [misc.getUserInfo(threads[i][0]) for i in range(len(threads))]
users1 = [users[i][j] for i in range(len(users)) for j in range(len(users[i]))]

usersAndRepToPostRatios = [(users1[i]['Username'], \
	int(users1[i]['Rep Power']), int(users1[i]['Posts'].replace(',', ''))) for i in range(len(users1))
for i in range(len(users1)) if int(users1[i]['Rep Power']) <= 200000]

print(len(usersAndRepToPostRatios)/3)

usersAndRepToPostRatios = list(set(usersAndRepToPostRatios))
usersAndRepToPostRatios.sort(key = lambda x:x[1])

top = usersAndRepToPostRatios[-15:]

print(top)

names = [top[i][0] for i in range(len(top))]
x = [top[i][1] for i in range(len(top))]
y = [top[i][2] for i in range(len(top))]

graph = misc.buildScatter(x, y, 'Best posters', text = names)

misc.dashIt(graph, "Miscer rankings in the first 6 pages of the misk", "Based on reps to posts ratio")
