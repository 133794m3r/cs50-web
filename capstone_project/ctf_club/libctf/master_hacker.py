#  Macarthur Inbody <admin-contact@transcendental.us>
#  Licensed under LGPLv3 Or Later (2020)
from random import randint
def maximum_tuple(tuples, start=0):
	maximum = sum(tuples[start])
	num = len(tuples)
	index = 0
	cur = 0
	for i in range(start + 1, num):
		cur = tuples[i][0] + tuples[i][1]
		if cur > maximum:
			maximum = cur
			index = i
	return index


def total_value(comb, max_storage):
	total_storage = total_value = 0
	for storage, value in comb:
		total_storage += storage
		total_value += value

	return (total_value, total_storage) if total_storage <= max_storage else (0, 0)


def master_hacker(max_storage, items):
	number_of_items = len(items)
	drive = [[-1 for j in range(max_storage + 1)] for i in range(number_of_items + 1)]
	max_items = number_of_items + 1
	max_storage_1 = max_storage + 1
	for i in range(1, number_of_items + 1):
		storage, value = items[i - 1]
		for s in range(1, max_storage + 1):
			if storage > s:
				drive[i][s] = drive[i - 1][s]
			else:
				drive[i][s] = max(drive[i - 1][s], drive[i - 1][s - storage] + value)

	flash_drive = []
	m = max_storage
	for i in range(number_of_items, 0, -1):
		prev_added = drive[i][m] != drive[i - 1][m]

		if prev_added:
			storage, value = items[i - 1]
			flash_drive.append(items[i - 1])
			m -= storage

	return flash_drive


# items
# TODO: Actually come up with a list of possible item names.
"""
Then I'll actually pull from that list to get my string.
Their flag will be something like items
"""


def make_tuples(number_of_items, max_storage):
	from random import randint
	tuples = []
	max_value = max_storage // 2
	for i in range(number_of_items + 1):
		tuples.append((randint(10, max_storage), randint(1, max_value)))
	return tuples


def make_filenames(number_of_items):
	item_prefixes = ['SECRET', 'WIP', 'BACKUP', 'FINAL', 'BOOK', 'VOLUME', 'PLAY', 'ARCHIVE', 'PRAWN', 'PWN', 'PASSWORDS',
	                 'KEY_VAULT', 'KEYS', 'BUSINESS_REPORTS', 'TOTALLY_LEGIT_EMAIL']
	item_prefixes_len = len(item_prefixes) - 1
	item_suffixes = ['zip', '7z', 'rar', 'img', 'iso', 'txt', 'tgz', 'bz', 'xz', 'lz4', 'db', 'sql', 'csv', 'doc', 'docx', 'enc',
	                 'eml']
	item_suffixes_len = len(item_suffixes) - 1
	filenames = []
	filename = ''
	j = 0
	k = 0
	for i in range(number_of_items):
		j = randint(0, item_prefixes_len)
		k = randint(0, item_suffixes_len)
		filename = '{1}-{0}.{2}'.format(i, item_prefixes[j], item_suffixes[k])
		filenames.append(filename)
	return filenames

def solve_masterhacker(tuples,filenames):
	pass

def make_masterhacker():
	max_storage = randint(50, 400)
	number_of_items = randint(100, 200)
	chal_msg = f"""<p>You've broken into a remote computer system. You've already gotten archives that hold {number_of_items //2} items of value. You need to figure out from the list of items left on the computer that you can steal. You only have {max_storage}MiB of data left. You've already run an enumerator on the drive and have a list of tuples for the items that you can get You need to go through this tuple and get as many pieces of information as possible while still not going over your budget since you have to flee the seen and cover up your tracks before you're caught. There are still {number_of_items} items left on the device to sift through.The answer must be returned in a tuple. The file contains three csv lists. The first is the filenames, second is the storage space required and the third is value of each of the items</p>"""
	#.format(
	#	max_storage, number_of_items // 2, number_of_items))
	tuples = make_tuples(number_of_items, max_storage)

	tuples_listed = list(map(list, zip(*tuples)))
	filenames = make_filenames(number_of_items)
	filenames_write = ','.join(filenames)
	storages = ','.join([str(x) for x in tuples_listed[0]])
	values = ','.join([str(x) for x in tuples_listed[1]])
	with open('files/analyzed_data_output.txt', 'w') as tuple_file:
		tuple_file.write('{}\n{}\n{}\n'.format(filenames_write, storages, values))

	bagged = master_hacker(max_storage, tuples)
	max_tuple_index = maximum_tuple(bagged)


	#max_tuple = bagged[max_tuple_index]
	max_tuple_fname = filenames[max_tuple_index]
	#print("The max tuple was {} and it's filename was {}".format(max_tuple, max_tuple_fname))

	chal_msg += "&lt;FILENAME OF HIGHEST VALUED ITEM&gt;;&lt;#_of_items&gt;;(&lt;total_value&gt;,&lt;total_storage_used&gt;)"
	val, stg = total_value(bagged, max_storage)

	#print('\ntv:{0}, wt:{1}'.format(val, stg))
	#print("\n{};{};({},{})\n".format(max_tuple_fname, len(bagged), val, stg))
	flag = f"""{max_tuple_fname};{len(bagged)};({val},{stg})"""

	#Now making the test-case for them.
	max_storage = randint(20,40)
	number_of_items = randint(3,5)
	filenames = make_filenames(number_of_items)
	filenames_write = ','.join(filenames)
	storages = ','.join([str(x) for x in tuples_listed[0]])
	values = ','.join([str(x) for x in tuples_listed[1]])
	bagged = master_hacker(max_storage,tuples)
	max_tuple_index = maximum_tuple(bagged)
	max_tuple_fname = filenames[max_tuple_index]
	val, stg = total_value(bagged,max_storage)

	chal_msg += f"""<p> Your testcase is below.</p><p class="text-monospace">{filenames_write}<br />{storages}<br />{values}</p><br />The answer to the testcase would then be: {max_tuple_fname};{len(bagged)};({val},{stg})"""

	return chal_msg,flag,"analyzed_data_output.txt"

