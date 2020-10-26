import subprocess
import sys, getopt
import io

#creates file, writes specific problem to a file, lauches RE
def set_up_re(cyclic_input, file_name, iterations, star_size): 
	problem_output = []
	print("\n*LAUNCHING RE WITH " + str(iterations) + " ITERATIONS ON " + str(star_size) + "-REGULAR GRAPH" + " *\n")
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

#launches RE, with specific input problem, retrieves the output
def launchRoundElim(file_name, iterations): 
	output = None
	try: 
		process = subprocess.run(["target/release/server", "file", "--file", file_name, "--iter", iterations], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
		output = process.stdout
		#print('The output is:\n', process.stdout)
	except:
		print('The error is: ', process.stderr)
		print("The exit code was: %d" % process.returncode)
		sys.exit(1)
	return output