from generator import *
from output_analyzer import * 
from launcher import *
from displayer import *

def star_covers(file_name, iterations, regularity): 
	#create raw input to RE wrt star size
	active_fixed, active_perm, passive = generate_raw_input(regularity)
	#formulate a list of strings, where each string is a specific form of a problem to RE
	cyclic_input, problem_types = formulate_problems(active_fixed, active_perm, passive)

	problem_output = None
	analyzed_output = None
	divergent_problems = None
	relaxations = None 
	canonical = None 
	relaxation_types = None
	relaxation_output = None
	analyzed_relaxations = None

	command = input("Problems in canonical form are formulated, do you want to display the input? [Y/N]: ")

	while True:
		if (command == "Y" or command == "y"):
			display_cyclic_input(cyclic_input)
			break
		elif (command == "N" or command == "n"):
			break
		else:
			command = input("Unknown command, please type [Y/N]: ")

	command_1 = input("Continue with round-eliminating? [Y/N]: ")

	while True:
		if (command_1 == "Y" or command_1 == "y"): 
			#consecutively write problems to .txt and feed to re, retrieve results
			problem_output = set_up_re(cyclic_input, file_name, iterations, regularity)
			#analyze the output of re problems
			analyzed_output = check_approximate_convergence(problem_output)
			#present results
			divergent_problems = display(analyzed_output, problem_types, cyclic_input, regularity)
			break
		elif (command_1 == "N" or command_1 == "n"):
			print("Shutting down round-eliminator analyzer.")
			sys.exit(0)
		else: 
			command_1 = input("Unknown command, please type [Y/N]: ")

	command_2 = input("Display divergent non-fixed point problems? [Y/N]: ")

	while True:
		if (command_2 == "Y" or command_2 == "y"):
			test_divergent(divergent_problems, regularity)
			break
		elif (command_2 == "N" or command_2 == "n"):
			break
		else:
			command_2 = input("Unknown command, please type [Y/N]: ")


	command_3 = input("Relax divergent problems? [Y/N]: ")

	while True:
		if (command_3 == "Y" or command_3 == "y"): 
			#relax the divergent problems
			relaxations, canonical, relaxation_types = relax_problem(divergent_problems, regularity)
			break
		elif (command_3 == "N" or command_3 == "n"): 
			print("Shutting down round-eliminator analyzer.")
			sys.exit(0)
		else: 
			command_3 = input("Unknown command, please type [Y/N]: ")

	command_4 = input("Problems are relaxed. Display relaxations? [Y/N]: ")

	while True:
		if (command_4 == "Y" or command_4 == "y"):
			display_relaxations(relaxations, canonical, relaxation_types)
			break
		elif (command_4 == "N"or command_4 == "n"):
			break
		else: 
			command_4 = input("Unknown command, please type [Y/N]: ")

	command_5 = input("Continue with round-eliminating? [Y/N]: ")

	while True:
		if (command_5 == "Y" or command_5 == "y"):
			#feed the relaxations
			relaxation_output = set_up_re(relaxations, file_name, iterations, regularity)

			#analyze the output of re relaxations
			analyzed_relaxations = check_approximate_convergence(relaxation_output)

			#present results of relaxations
			display(analyzed_relaxations, relaxation_types, relaxations, regularity)
			break
		elif (command_5 == "N" or command_5 == "n"):
			print("Shutting down round-eliminator analyzer.")
			sys.exit(0)
		else:
			command_5 = input("Unknown command, please type [Y/N]: ")