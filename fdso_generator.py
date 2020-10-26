import io
import sys
import itertools

# fdso representation is taken from the paper
# Classification of Distributed Binary Labeling Problems
# A X^(d-1)
# H^(s+1) X^(d-s-1)
# T^(d-s+1) X^(s-1)
#
#X AHTX(δ-1)
#HT AHTX(δ-2)
def get_fdso_problem(white_d, black_d): 

	problems = []
	problem_types = []
	a = 'A'
	x = 'X'
	t = 'T'
	h = 'H'
	sep = ' '
	
	#generate fdso problems iteratively
	for i in range(white_d - 1): 
		forbidden_d = i + 1
		act_line1 = a + sep + (x + sep) * (white_d - 1)
		act_line2 = (h + sep) * (forbidden_d + 1) + (x + sep) * (white_d - forbidden_d - 1)
		act_line3 = (t + sep) * (white_d - forbidden_d + 1) + (x + sep) * (forbidden_d - 1)

		pas_line1 = x + sep + (a + h + t + x + sep) * (black_d - 1)
		pas_line2 = h + sep + t + sep + (a + h + t + x + sep) * (black_d - 2)

		instance = act_line1 + '\n' + act_line2 + '\n' + act_line3 + '\n\n' + pas_line1 + '\n' + pas_line2

		problem_type = (white_d, black_d, forbidden_d)

		problems.append(instance)

		problem_types.append(problem_type)

	return problems, problem_types