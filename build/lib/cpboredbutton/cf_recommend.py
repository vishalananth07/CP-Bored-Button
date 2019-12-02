import functools
import random
import requests

CONST_RATING_UPPERBOUND = 300
CONST_RATING_LOWERBOUND = 100

CONST_MIN_SOLVED_PROBLEM = 13
CONST_AVERAGE_LIMIT = 100
CONST_MIN_RATING_AVERAGE = 1000


def get_problem_url(user_rating, problem_list):
    filtered_problem = [i for i in problem_list if i['rating'] >= user_rating - CONST_RATING_LOWERBOUND and i[
        'rating'] <= user_rating + CONST_RATING_UPPERBOUND]
    if len(filtered_problem) == 0:
        greater_than_upper = [i for i in problem_list if i['rating'] > user_rating + CONST_RATING_UPPERBOUND]
        less_than_lower = [i for i in problem_list if i['rating'] < user_rating - CONST_RATING_LOWERBOUND]
        if len(greater_than_upper) > 0:
            min_of_max = min(greater_than_upper, key=lambda x: x['rating'])
            filtered_problem.append(min_of_max)
        if len(less_than_lower) > 0:
            max_of_min = max(less_than_lower, key=lambda x: x['rating'])
            filtered_problem.append(max_of_min)
    if len(filtered_problem) == 0:
        print("You've Solved Everything")
    random_problem = random.choice(filtered_problem)
    return "https://codeforces.com/problemset/problem/" + str(random_problem['contestId']) + "/" + random_problem[
        'index']


def get_limit(x):
    if x > CONST_MIN_SOLVED_PROBLEM:
        x = (x / 5) + 10
    return int(min(x, CONST_AVERAGE_LIMIT))


def calculate_rating_average(solved_problems):
    limit = get_limit(len(solved_problems))
    if limit == 0:
        return CONST_MIN_RATING_AVERAGE
    rating_average = 0
    for i in range(0, limit):
        rating_average += solved_problems[i]['rating']
    rating_average /= limit
    return rating_average


def remove_duplicate(solved_problems):
    n = len(solved_problems)
    s_problems = []
    for i in range(1, n):
        if solved_problems[i] != solved_problems[i - 1]:
            s_problems.append(solved_problems[i - 1])
    return s_problems


def sort_rating_comparator(problem1, problem2):
    if problem1['rating'] < problem2['rating']:
        return 1
    else:
        return -1


def sort_problem_comparator(problem1, problem2):
    if problem1['contestId'] != problem2['contestId']:
        if problem1['contestId'] < problem2['contestId']:
            return 1
        else:
            return -1
    else:
        if problem1['index'] < problem2['index']:
            return 1
        else:
            return -1


def remove_solved(solved_problems, all_problems_wr):
    unsolved_problems = []
    i = 0
    for problem in all_problems_wr:
        if i == len(solved_problems) or problem != solved_problems[i]:
            unsolved_problems.append(problem)
        else:
            i += 1
    return unsolved_problems


def get_random_problem(user_handle):
    # Fetching handle
    resp = requests.get("https://codeforces.com/api/user.status?handle=" + user_handle + "&from=1")
    if resp.status_code < 200 or resp.status_code > 299:
        print("Error " + resp.status_code + "\nCould not fetch handle")
        quit()

    # Fetching solved problems
    all_attempted_problems = resp.json()['result']
    solved_problems = []
    for problem in all_attempted_problems:
        if "rating" in problem['problem'] and problem['verdict'] == "OK":
            solved_problems.append({"contestId": problem['problem']['contestId'], "index": problem['problem']['index'],
                                    "rating": problem['problem']['rating']})

    # Fetching all problems
    resp = requests.get("https://codeforces.com/api/problemset.problems")
    if resp.status_code < 200 or resp.status_code > 299:
        print("Error " + resp.status_code + "\nCould not fetch problems")
        quit()
    all_problems = resp.json()['result']['problems']
    all_problems_wr = []
    for problem in all_problems:
        if "rating" in problem:
            all_problems_wr.append(
                {"contestId": problem['contestId'], "index": problem['index'], "rating": problem['rating']})

    solved_problems = sorted(solved_problems, key=functools.cmp_to_key(sort_problem_comparator))
    all_problems_wr = sorted(all_problems_wr, key=functools.cmp_to_key(sort_problem_comparator))

    unsolved_problems = remove_solved(solved_problems, all_problems_wr)

    solved_problems = remove_duplicate(solved_problems)
    solved_problems = sorted(solved_problems, key=functools.cmp_to_key(sort_rating_comparator))

    rating_average = calculate_rating_average(solved_problems)

    cf_url = get_problem_url(rating_average, unsolved_problems)

    return cf_url