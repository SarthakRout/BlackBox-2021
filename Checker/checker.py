import os
import subprocess
import copy

base_path = "C:\\Users\\user\\Documents\\Y20_BB\\BlackBox"
taxi_exec_path = "C:\\Users\\user\\Documents\\Y20_BB\\Taxi"

def Check(team, qid, case_input, case_output, script_path):
	res = ""
	try:
		p = subprocess.run([taxi_exec_path, script_path], stdout = subprocess.PIPE, input=case_input, encoding='utf-8', timeout=1)
		res = p.stdout
		if res == None:
			print(team + ' QID: ' + str(qid) + ': Program Terminated Unsuccessfully with None Type Output')
			return 0
		res = res.splitlines()
		if len(res)<4:
			print(team  + ' QID: ' + str(qid) + ' : Program Terminated Unsuccessfully with some Errors : ')
			print(res)
			return 0
		result = str(res[3])

		# Allowing for Curly Double Quotes in solution
		result = result.replace("“", "")
		result = result.replace("”", "")

		if(case_output.isnumeric()):
			if(int(float(result)) == int(case_output)):
				return 1
			else:
				print(team + ' QID: ' + str(qid) + ' ' + result + ' ' + case_output + ' : Incorrect Answer')
				return 0
		elif result == (case_output):
			return 1
		else:
			print(team +  ' QID: ' + str(qid) +  ' ' + result + ' ' + case_output + ' : Incorrect Answer')
			return 0
	except subprocess.TimeoutExpired:
		print("Process Terminated due to Timeout (Infinite Loop): " + team + ' QID : ' +  str(qid))
		return 0

def Evaluate(team, qid, test_cases):
	script_path = base_path + "\\" + team + "\\" + str(qid) + ".txt"
	if(os.path.exists(script_path)==False):
		print(team + ' has not solved question ' + str(qid) + '.')
		return -1
	# Evaluate test cases for a question
	for test_case in test_cases:
		case = test_case.split(':')
		case_input = case[0]
		case_output = case[1]
		# Check for one test case for a question for a team
		response = Check(team, qid, case_input, case_output, script_path)
		if(response==0):
			print(team + ' has solved the question ' + str(qid) + ' incorrectly.')
			return 0
	print(team + ' has solved the question ' + str(qid) + ' correctly.')
	return 1

# Load Test Cases
f = open('tests.txt');
test_cases = {}
qid = 1
for line in f.readlines():
	cases = line.split(",");
	cases_new = [];
	for case in cases:
		case = case.replace("\"", "");
		case = case.replace("\n", "");
		cases_new.append(case);
	test_cases[qid] = cases_new;
	qid = qid + 1;
f.close()

# Load Teams
teams = os.listdir(base_path)

# Make Default Report
def_report = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

result = {}

for team in teams:
	report = copy.deepcopy(def_report)
	# Evaluate a team
	for i in range(1, 10):
		# Evaluate one question for a team
		report[i] = Evaluate(team, i, test_cases[i])
	result[team] = report

print(result)

f = open('results.txt', mode='w', encoding='utf-8')
for team in teams:
	s = team + ' '
	for i in range(1, 10):
		s = s + ',' + str(result[team][i]) + ' '
	s = s + '\n'
	f.write(s)
f.close()