import requests
import json
import random
import os
import functools


def getProblemURL(user_rating,problem_list):
	filtered_problem = [i for i in problem_list if i['rating']>=user_rating-100 and i['rating']<=user_rating+300]
	if len(filtered_problem) == 0:
		greater_than_upper = [i for i in problem_list if i['rating']>user_rating+300]
		less_than_lower = [i for i in problem_list if i['rating']<user_rating-100]
		if len(greater_than_upper) > 0:
			min_of_max = min(greater_than_upper,key = lambda x:x['rating'])
			filtered_problem.append(min_of_max)
		if len(less_than_lower) > 0:
			max_of_min = max(less_than_lower,key = lambda x:x['rating'])
			filtered_problem.append(max_of_min)
	if len(filtered_problem) == 0:
		print("You've Solved Everything")		
	random_problem = random.choice(filtered_problem)
	#https://codeforces.com/problemset/problem/contestId/index
	return "https://codeforces.com/problemset/problem/"+str(random_problem['contestId'])+"/"+random_problem['index']


def calRatingAvg(solved_problems):
	lim = 0
	if len(solved_problems) <= 13:
		lim = len(solved_problems)
	else:
		lim = (len(solved_problems)/5) + 10
	lim = min(lim,100)
	it = 0
	rating_average = 0
	while it<lim:
		rating_average += solved_problems[it]['rating']
		it = it + 1
	rating_average/=it
	if rating_average==0:
		rating_average = 1000
	return rating_average


def removeDupli(solved_problems):
	n = len(solved_problems)
	s_problems = []
	for i in range(1,n):
		if(solved_problems[i] != solved_problems[i-1]):
			s_problems.append(solved_problems[i-1])
	return s_problems


def sortFuncRat(problem1,problem2):
	if problem1['rating']<problem2['rating']:
		return 1
	else:
		return -1


def sortFunc(problem1,problem2):
	if problem1['contestId'] != problem2['contestId']:
		if problem1['contestId']<problem2['contestId']:
			return 1
		else:
			return -1
	else:
		if problem1['index']<problem2['index']:
			return 1
		else:
			return -1


def removeSolved(solved_problems,all_problems_wr):
	unsolved_problems = []
	i = 0
	for problem in all_problems_wr:
		if problem != solved_problems[i]:
			unsolved_problems.append(problem)
		else:
			i += 1
	return unsolved_problems
	

def getRandomProblem(user_handle):
	resp = requests.get("https://codeforces.com/api/user.status?handle="+ user_handle + "&from=1");
	if resp.status_code < 200 or resp.status_code>299:
		print("Error in Request : "+resp.url)
		quit()
	all_attempted_problems = resp.json()['result']
	solved_problems = []
	for problem in all_attempted_problems:
		if "rating" in problem['problem'] and problem['verdict'] == "OK":
			solved_problems.append({"contestId":problem['problem']['contestId'],"index":problem['problem']['index'],"rating":problem['problem']['rating']})

	resp = requests.get("https://codeforces.com/api/problemset.problems");
	if resp.status_code < 200 or resp.status_code>299:
		print("Error in Request : "+resp.url)
		quit()
	all_problems = resp.json()['result']['problems']
	all_problems_wr = []
	for problem in all_problems:
		if "rating" in problem:
			all_problems_wr.append({"contestId":problem['contestId'],"index":problem['index'],"rating":problem['rating']})

	solved_problems = sorted(solved_problems, key=functools.cmp_to_key(sortFunc))
	all_problems_wr = sorted(all_problems_wr, key=functools.cmp_to_key(sortFunc))

	unsolved_problems = removeSolved(solved_problems,all_problems_wr)

	solved_problems = removeDupli(solved_problems)
	solved_problems = sorted(solved_problems, key=functools.cmp_to_key(sortFuncRat))

	rating_average = calRatingAvg(solved_problems)

	cf_url = getProblemURL(rating_average,unsolved_problems)

	return cf_url
