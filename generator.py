import io
import sys
import itertools

#generates the raw input to the RE
def generate_raw_input(star_size): 
	active = []
	active_permutations = []
	separator = ' '

	#first line of input is fixed
	for i in range(star_size): 
		if i is (star_size - 1):
			active.append('C')
		else: 
			active.append('A')

	#create list of all possible label-combinations for all variable strings
	combinations = list(itertools.product(['A', 'B'], repeat=star_size))

	#sort labels in each string
	for i in range(len(combinations)):
		combinations[i] = tuple(sorted(combinations[i]))

	#remove dublicates
	combinations = list(dict.fromkeys(combinations))
	del combinations[0]
	#print(combinations)

	#permute all tuples to obtain all possible combinations
	star = 1
	while star <= star_size:
		permutations = list(itertools.permutations(combinations, star))
		#print(permutations)
		#sort each permutation pair
		for i in range(len(permutations)):
			permutations[i] = tuple(sorted(permutations[i]))

		#remove permutation-pair dublicates
		active_permutation = list(dict.fromkeys(permutations))
		#print(active_permutation)
		active_permutations.append(active_permutation)

		star += 1
	#print(permutations)
	#print("----")

	active = separator.join(active)

	#passive labels are fixed
	passive = "A A\nB C\n"

	#print(active)
	#print(active_permutations)
	#print(passive)

	return active, active_permutations, passive

#formulates specific problem to be fed to RE and check the problem type
def formulate_problems(active_fixed, active_permutations, passive): 
	separator = ' '
	cyclic_input = []
	problem_types = []
	sub = 'B'
	for subclass in range(len(active_permutations)): 
		for problem in range(len(active_permutations[subclass])):
			#create active block of labels
			active = active_fixed
			#store problem types
			stars = []
			for ix in range(len(active_permutations[subclass][0])):
				active = active + "\n" + separator.join(list(active_permutations[subclass][problem][ix]))
				stars.append(str(active_permutations[subclass][problem][ix]).count(sub))
			#add passive block
			inp = active + "\n" + "\n" + passive
			cyclic_input.append(inp)
			problem_types.append(stars)
			active = ""
			#print(cyclic_input)
	return cyclic_input, problem_types

#test function to see the form of relaxations used for testing during development
def display_relaxations(relaxations, canonical, relaxation_types): 
	for i in range(len(relaxations)): 
		print("\n(" + str(i + 1) + ")\n")
		print("Covering problem with stars: " + str(relaxation_types[i]) + "\n\n<=>\n\n" + canonical[i] + '\n\n' + '=>' + '\n\n' + relaxations[i])


# BE^(δ-(k-1)) CDE ABCDE^(k-2)
# DE^(k+1) ABCDE^(δ-(k+1))
# E ABCDE^(δ-1)

#relax the representations of divergent problems
def relax_problem(divergent_problems, delta):
	#print(delta)

	#initialize constants and containers
	relaxations = []
	canonical = []
	a = 'BE'
	b = 'DE'
	bc = 'CDE'
	c = 'CE'
	ab = 'ABCDE'
	passive = '\n\n' + 'B B\nD C\nA E'
	line3 = 'E ' + (ab + ' ') * (delta - 1)
	#print(divergent_problems[0][1])

	#first, handle the case δ=n, k=1

	boundary_problem_1 = divergent_problems[len(divergent_problems) - 1][1].split("\n")
	#print(boundary_problem_1)

	filtered_1 = list(filter(lambda x: len(x) > delta, boundary_problem_1))
	#print(filtered_1)

	filtered_1 = [list(filter(lambda c: c != ' ', string)) for string in filtered_1]
	#print(filtered_1)

	line1 = filtered_1[0]
	#print(line1)
	filtered_1.pop(0)
	unzipped_1 = tuple(zip(*filtered_1))
	#print(unzipped_1)

	contraction_1 = ["".join(sorted(list(dict.fromkeys(ins)))) for ins in unzipped_1]
	#print(contraction_1)

	canonical_conraction_1 = ' '.join(line1) + "\n" + ' '.join(contraction_1) + "\n\n" + "A A\nB C\n"
	#print(canonical_conraction)

	#perform substition 
	line1 = [a if x == 'A' else c for x in line1]
	r_contraction_1 = [ab if x == 'AB' else b for x in contraction_1]

	#concatenate
	problem_1 = ' '.join(line1) + '\n' + ' '.join(r_contraction_1) + '\n' + line3 + passive
	#print(problem_1)
	relaxations.append(problem_1)

	#canonical form
	canonical.append(canonical_conraction_1)


	# use algorithm below to formulate non-boundary cases when (δ!=k && k!=1) or star_size > 3
	#
	# BE^(δ-(k-1)) CDE ABCDE^(k-2)
	# DE^(k+1) ABCDE^(δ-(k+1))
	# E ABCDE^(δ-1)
	if (delta != 3): 
		for i in range(delta - 2):
			k = i + 2
			line1 = (a + ' ') * (delta - (k - 1)) + (bc + ' ') + (ab + ' ') * (k - 2) + '\n'
			line2 = (b + ' ') * (k + 1) + (ab + ' ') * (delta - (k + 1)) + '\n'
			problem_i = line1 + line2 + line3 + passive
			#print(problem_i)
			relaxations.append(problem_i)
			#insert canonical problem
			canonical.append(divergent_problems[len(divergent_problems) - k][1])
			#canonical.append(divergent_problems[i][1])
		
	#finally, handle boundary case δ=k

	#split the problem
	boundary_problem_n = divergent_problems[0][1].split("\n")
	#print(boundary_problem_1)

	#filter passive versions
	filtered_n = list(filter(lambda x: len(x) > delta, boundary_problem_n))
	#print(filtered_)

	#filter the empty characters
	filtered_n = [list(filter(lambda c: c != ' ', string)) for string in filtered_n]
	#print(filtered_)

	#unzip ractive version to begin contraction
	unzipped_n = tuple(zip(*filtered_n))
	#print(unzipped)

	#contract to one-line form
	contraction_n = ["".join(sorted(list(dict.fromkeys(ins)))) for ins in unzipped_n]
	#print(contraction)

	canonical_conraction_n = ' '.join(contraction_n) + "\n\n" + "A A\nB C\n"

	#perform substition 
	r_contraction_n = [a if x == 'A' else ab if x == 'AB' else bc for x in contraction_n]
	#print(r_contraction)
	r_contraction_n = ' '.join(r_contraction_n)
	#print(r_contraction)

	#concatenate
	problem_n = r_contraction_n + '\n' + line3 + passive
	#print(problem_1)
	relaxations.append(problem_n)
	canonical.append(canonical_conraction_n)

	relaxation_types = []
	for i in range(len(divergent_problems)): 
		relaxation_types.append(divergent_problems[len(divergent_problems) - 1 - i][0])
		#print(relaxation_types[i])

	#test
	#display_relaxations(relaxations, canonical, relaxation_types)

	return relaxations, canonical, relaxation_types