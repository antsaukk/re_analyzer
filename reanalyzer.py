import subprocess
import io
import sys, getopt
from generator import *
from output_analyzer import * 

#launches RE, with specific input problem, retrieves the output
def launchRoundElim(file_name, iterations): 
	#process = subprocess.run(["target/release/server", "file", "--file", "test.txt", "--iter", "12"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
	process = subprocess.run(["target/release/server", "file", "--file", file_name, "--iter", iterations], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
	output = process.stdout
	#print('The output is:\n', process.stdout)
	#print('---------------------------------------\n')
	#print('The error is: ', process.stderr)
	#print("The exit code was: %d" % process.returncode)
	return output

#test cyclic input to RE
def test_ci(cyclic_input): 
	#print("-------------------TEST START-------------------")
	for i in range(len(cyclic_input)):
		print("Problem " + str(i + 1) + ": ")
		print(cyclic_input[i])
	#print("-------------------TEST FINISHED-------------------")


#creates file, writes specific problem to a file, lauches RE
def set_up_re(cyclic_input, file_name, iterations, star_size): 
	#output collection
	problem_output = []

	print("\n*LAUNCHING RE WITH " + str(iterations) + " ITERATIONS AND STAR SIZE " + str(star_size) + " *\n")
	for i in range(len(cyclic_input)): 
		file = open(file_name, "w+")
		file.write(cyclic_input[i])
		file.close()
		print("ROUND-ELIMINATING PROBLEM: " + str(i + 1) + " ")
		re_output = launchRoundElim(file_name, iterations)
		problem_output.append(re_output)
		print("Done. Output collected.")
		#break
	return problem_output

#print the results
def display(analyzed_output, problem_types, cyclic_input, star_size): 
	#collection of not fixed point problems
	divergent_instances = []
	for i in range(len(analyzed_output)): 
		if analyzed_output[i] is True: 
			print(str(i + 1) + ": Covering problem of the " + str(star_size) + " regular graph with stars of sizes " + str(problem_types[i]) + " most probably diverges.")
			if (len(problem_types[i]) == star_size - 1): 
				d_inst = (problem_types[i], cyclic_input[i])
				divergent_instances.append(d_inst)
		else: 
			print(str(i + 1) + ": Covering problem of the " + str(star_size) + " regular graph with stars of sizes " + str(problem_types[i]) + " possibly converges.")
	return divergent_instances

#display divergent problems
def test_divergent(divergent_problems, star_size): 
	print("\nProblems of star size " + str(star_size) + " not converging to any fixed point:\n\n")
	for i in range(len(divergent_problems)):
		print("(" + str(i + 1) + ") problem type: ")
		print(divergent_problems[i][0])
		print("\nproblem definition: ")
		print(divergent_problems[i][1])

#test function to see the form of relaxations
def display_relaxations(relaxations, canonical, relaxation_types): 
	print('\n-------------------ABCDE RELAXED PROBLEMS-------------------')
	for i in range(len(relaxations)): 
		print("\n(" + str(i + 1) + ")\n")
		print("Covering problem with stars: " + str(relaxation_types[i]) + "\n\n<=>\n\n" + canonical[i] + '\n\n' + 'A => B + E' + '\n\n' + 'B => D + E' + '\n\n'
		+ 'C => C + E' + '\n\n' + '+ E ABCDE * (delta - 1)' + '\n\n' + relaxations[i])

#user instructions
def usage():
	print('reanalyzer.py --file <file.txt> --iterations <iterations> --star_size <star-size>')
	print('\nflags: \n-h for help \n--file <file.txt> to write problems \n--iterations <iterations> of round eliminator \n--star_size <star-size> regularity of the graph\n')

def main():
	try: 
		opts, args = getopt.getopt(
			sys.argv[1:], 
			"ho:v", 
			[
			"help",
			"file_name=", 
			"iterations=",
			"star_size="
			])
	except getopt.GetoptError as err: 
		print(err)
		usage()
		sys.exit(2)

	file_name = None
	iterations = None
	star_size = 0
	flag = None

	#retrieve CL arguments
	for opt, arg in opts: 
		if opt == "--file_name":
			file_name = arg
		elif opt == "--iterations":
			iterations = arg
		elif opt == "--star_size": 
			star_size = int(arg)
		elif opt in("-h", "--help"):
			usage()
			sys.exit()
		else:
			print("Uknown command: " + opt)
			sys.exit(1)

	if star_size <= 2:
		print("\n-Please consider problems of size >= 3-\n")
		sys.exit(1)
	#file_name, iterations, star_size = sys.argv[1:][0], sys.argv[1:][1], int(sys.argv[1:][2])

	try: 
		#create raw input to RE wrt star size
		active_fixed, active_perm, passive = generate_raw_input(star_size)
	
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
			if (command == "Y"):
				#test
				test_ci(cyclic_input)
				break
			elif (command == "N"):
				break
			else:
				command = input("Unknown command, please type [Y/N]: ")
				#sys.exit(2)

		command_1 = input("Continue with round-eliminating? [Y/N]: ")

		while True:
			if (command_1 == "Y"): 
				#consecutively write problems to .txt and feed to re, retrieve results
				problem_output = set_up_re(cyclic_input, file_name, iterations, star_size)
		
				#analyze the output of re problems
				analyzed_output = check_approximate_convergence(problem_output)
		
				#present results
				divergent_problems = display(analyzed_output, problem_types, cyclic_input, star_size)
				break
			elif (command_1 == "N"):
				print("Shutting down round-eliminator analyzer.")
				sys.exit(0)
			else: 
				command_1 = input("Unknown command, please type [Y/N]: ")

		command_2 = input("Display divergent non-fixed point problems? [Y/N]: ")

		while True:
			if (command_2 == "Y"):
				#test
				test_divergent(divergent_problems, star_size)
				break
			elif (command_2 == "N"):
				break
			else:
				command_2 = input("Unknown command, please type [Y/N]: ")


		command_3 = input("Relax divergent problems? [Y/N]: ")

		while True:
			if (command_3 == "Y"): 
				#relax the divergent problems
				relaxations, canonical, relaxation_types = relax_problem(divergent_problems, star_size)
				break;
			elif (command_3 == "N"): 
				print("Shutting down round-eliminator analyzer.")
				sys.exit(0)
			else: 
				command_3 = input("Unknown command, please type [Y/N]: ")

		command_4 = input("Problems are relaxed. Display relaxations? [Y/N]: ")

		while True:
			if (command_4 == "Y"):
				display_relaxations(relaxations, canonical, relaxation_types)
				break
			elif (command_4 == "N"):
				break
			else: 
				command_4 = input("Unknown command, please type [Y/N]: ")

		command_5 = input("Continue with round-eliminating? [Y/N]: ")

		while True:
			if (command_5 == "Y"):
				#feed the relaxations
				relaxation_output = set_up_re(relaxations, file_name, iterations, star_size)

				#analyze the output of re relaxations
				analyzed_relaxations = check_approximate_convergence(relaxation_output)

				#present results of relaxations
				display(analyzed_relaxations, relaxation_types, relaxations, star_size)
				break
			elif (command_5 == "N"):
				print("Shutting down round-eliminator analyzer.")
				sys.exit(0)
			else:
				command_5 = input("Unknown command, please type [Y/N]: ")

	except:
		print("Ooop...sorry I died. (or got killed) :(")
		sys.exit(1)

	sys.exit(0)

if __name__ == "__main__":
	main()
