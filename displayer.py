

#test function to display cyclic input to RE, also used for user interaction
def display_cyclic_input(cyclic_input): 
	#print("-------------------TEST START-------------------")
	for i in range(len(cyclic_input)):
		print("\nProblem " + str(i + 1) + ": \n")
		print(cyclic_input[i])
	#print("-------------------TEST FINISHED-------------------")

#dispkay the results of round elimination
def display(analyzed_output, problem_types, cyclic_input, regularity): 
	divergent_instances = []
	print("here")
	for i in range(len(analyzed_output)): 
		if analyzed_output[i] is True: 
			print(str(i + 1) + ": Covering problem of the " + str(regularity) + " regular graph with stars of sizes " + str(problem_types[i]) + " most probably diverges.")
			if (len(problem_types[i]) == regularity - 1): 
				d_inst = (problem_types[i], cyclic_input[i])
				divergent_instances.append(d_inst)
		else: 
			print(str(i + 1) + ": Covering problem of the " + str(regularity) + " regular graph with stars of sizes " + str(problem_types[i]) + " possibly converges.")
	return divergent_instances

#display divergent problems
def test_divergent(divergent_problems, regularity): 
	print("\nProblems of star size " + str(regularity) + " not converging to any fixed point:\n\n")
	for i in range(len(divergent_problems)):
		print("(" + str(i + 1) + ") problem type: ")
		print(divergent_problems[i][0])
		print("\nproblem definition: ")
		print(divergent_problems[i][1])
		
#display form of relaxation to user
def display_relaxations(relaxations, canonical, relaxation_types): 
	print('\n-------------------ABCDE RELAXED PROBLEMS-------------------')
	for i in range(len(relaxations)): 
		print("\n(" + str(i + 1) + ")\n")
		print("Covering problem with stars: " + str(relaxation_types[i]) + "\n\n<=>\n\n" + canonical[i] + '\n\n' + 'A => B + E' + '\n\n' + 'B => D + E' + '\n\n'
		+ 'C => C + E' + '\n\n' + '+ E ABCDE * (delta - 1)' + '\n\n' + relaxations[i])