import subprocess
import io
import sys, getopt
from generator import *
from output_analyzer import * 
from fdso_generator import * 
from launcher import *
from displayer import *
from star_covers import *
from fdso import *

#user instructions
def usage():
	print('reanalyzer.py --file <file.txt> --iterations <iterations> --regularity <star-size>')
	print('\nflags: \n-h for help \n--file <file.txt> to write problems \n--iterations <iterations> of round eliminator \n--regularity <regularity> regularity of the graph\n --flag <flag> type of problem')
	print("\n\n Problem types: \n -sc - star-covers\n -fd - forbidden degree sinkless orientation")

#is bugged - still fix the input taking
def main():
	try: 
		opts, args = getopt.getopt(
			sys.argv[1:], 
			"ho:v", 
			[
			"help",
			"file_name=", 
			"iterations=",
			"regularity=", 
			"flag="
			])
	except getopt.GetoptError as error: 
		print(error)
		usage()
		sys.exit(1)

	file_name = None
	iterations = None
	regularity = 0
	flag = None
	flags = {"fd", "sc"}

	#retrieve CL arguments
	for opt, arg in opts: 
		if opt == "--file_name":
			file_name = arg
		elif opt == "--iterations":
			iterations = arg
		elif opt == "--regularity": 
			regularity = int(arg)
		elif opt == "--flag":
			flag = arg
		elif opt in("-h", "--help"):
			usage()
			sys.exit(0)
		else:
			print("Unknown command: " + opt)
			sys.exit(1)

	if regularity <= 2:
		print("\nPlease consider problems of size >= 3\n")
		sys.exit(1)

	if (flag in flags) is False: 
		print(flag)
		print("\nProblem is not recognized\n")
		sys.exit(1)

	try: 
		if (flag == "sc"):
			star_covers(file_name, iterations, regularity)
		elif (flag == "fd"):
			fdso(file_name, iterations, regularity)

	except:
		print("Ooop...sorry I died. (or got killed) :(")
		sys.exit(1) 

	sys.exit(0)

if __name__ == "__main__":
	main()
