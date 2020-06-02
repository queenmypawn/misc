import misc

phrase1 = "OP is a phaggot"
phrase2 = "Op is a phaggot"
phrase3 = "op is a phaggot"

phrase4 = "floyd"
phrase5 = "Floyd"
phrase6 = "murder"

phrase7 = "COVID"
phrase8 = "coronavirus"
phrase9 = "covid"
phrase10 = "Covid"
phrase11 = "virus"

op_is_a_phaggot_count = 0
protest_count = 0
covid_count = 0

threadsWithPostCounts = misc.getThreadsAndPostNumbers(pages = 1)

count = 0
for thread in threadsWithPostCounts:

	thread = thread[0] # Get only the thread from the (thread, post) tuple.

	op_is_a_phaggot_count += misc.searchPhraseInThread(
	thread = thread, 
	page_limit = 1,
	phrases = [phrase1, phrase2, phrase3],
	)

	protest_count += misc.searchPhraseInThread(
	thread = thread, 
	page_limit = 1,
	phrases = [phrase4, phrase5, phrase6],
	)

	covid_count += misc.searchPhraseInThread(
	thread = thread, 
	page_limit = 1,
	phrases = [phrase7, phrase8, phrase9, phrase10, phrase11],
	)
	print(count)
	count += 1

print('Total references were, in this order:')
print(f'George Floyd: {protest_count}')
print(f'Coronavirus: {covid_count}')
print(f"OP's sexual orientation: {op_is_a_phaggot_count}")
