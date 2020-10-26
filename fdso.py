from fdso_generator import *
from output_analyzer import * 
from launcher import *
from displayer import *

def fdso(file_name, iterations, regularity):

	delta = input("Please enter the value of delta as natural number: ")
	
	while True:
		try:
			delta = int(delta)
			break;
		except ValueError:
			delta = input("Please enter valid value of delta (as natural number): ")

	fdso_instances, problem_types = get_fdso_problem(regularity, delta)

	command = input("FDSO input is generated, do you want to display input? [Y/N]: ")

	while True:
		if (command == "Y" or command == "y"):
			display_cyclic_input(fdso_instances)
			break
		elif (command == "N" or command == "n"):
			break
		else:
			command = input("Unknown command, please type [Y/N]: ")

	command_1 = input("Continue with round-eliminating? [Y/N]: ")

	while True:
		if (command_1 == "Y" or command_1 == "y"): 
			problem_output = set_up_re(fdso_instances, file_name, iterations, regularity)

			analyzed_output = check_approximate_convergence(problem_output)

			divergent_problems = display(analyzed_output, problem_types, fdso_instances, regularity)
			break
		elif (command_1 == "N" or command_1 == "n"):
			print("Shutting down round-eliminator analyzer.")
			sys.exit(0)
		else: 
			command_1 = input("Unknown command, please type [Y/N]: ")

	