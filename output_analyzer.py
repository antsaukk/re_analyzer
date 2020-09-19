
#check if the problem diverges by identifying the system's interruption message
def check_approximate_convergence(problem_output):
	print("---Checking approximate convergence---")
	results = []
	panic_flag = "thread 'main' panicked"
	for i in range(len(problem_output)): 
		if panic_flag in problem_output[i]: 
			results.append(True)
		else:
			results.append(False)
	return results
