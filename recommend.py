from argparse import ArgumentParser
import cf_recommend
import random
import os
def getInput():
	#Define Input Here
	parser = ArgumentParser()
	parser.add_argument("-cf","--codeforces",required=True )
	args = parser.parse_args()
	user_handles = {
		"codeforces" : args.codeforces
		}
	return user_handles

def main():
	parameter = getInput()
	# Append all available OJs
	open_url = []
	if parameter["codeforces"] != None:
		open_url.append("codeforces")
	
	random_oj = random.choice(open_url)
	url = ""
	if random_oj == "codeforces":
		url = cf_recommend.getRandomProblem(parameter["codeforces"])
	os.system("xdg-open "+url+" 2>/dev/null")
if __name__ == "__main__":
	main()