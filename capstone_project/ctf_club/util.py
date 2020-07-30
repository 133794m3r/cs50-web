def make_index(objects):
	output = {}
	categories = []
	for challenge in objects:
		if output.get(challenge.category) is None:
			output[challenge.category] = [challenge]
			categories.append(challenge.category)
		else:
			output[challenge.category].append(challenge)

	return categories,output
