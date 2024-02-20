# -*- coding: utf-8 -*-
from git import Repo
from git import GitCommandError
import re


# Function to check whether modification done or not
def stchk (repository_path):
	repo = Repo(repository_path)
	try:
		status = repo.git.status()
		
		if "nothing to commit" in status:
			stat = "NO"
			return(stat)
		else:
			stat = "YES"
			return(stat)
	except GitCommandError as e:
		print(f"Error: {e}")


# Function to push modification done on GitHub
def git_commit_and_push(repository_path, commit_message):
    
    repo = Repo(repository_path)
    
    try:
    	status = repo.git.status()

    	lines = status.split('\n')

    	print("Do you want to view a list of the modified files? If yes, please enter 1. Otherwise, enter 0.\n")
    	user_chk = input()

    	if user_chk == "1":
    		for each in lines:
    			if "modified:" in each:
    				each = each.strip()
    				print (each)
    	print("\n")

    	repo.git.add('.')
    	diff = repo.git.diff('--staged')

    	print("Do you want to see the modifications made to the modified files? If so, enter Y. Otherwise, enter the letter N.\n")
    	user_opt = input()

    	if user_opt == "Y":
    		print (diff)

    	repo.git.commit('-m', commit_message)

    	if not repo.active_branch.tracking_branch():
    		upstream_branch = f'origin/{repo.active_branch.name}'
    		repo.git.branch('--set-upstream-to', upstream_branch)
    	
    	origin = repo.remote(name='origin')
    	origin.push()

    	print("Changes committed and pushed successfully.")

    except GitCommandError as e:
        print(f"Error: {e}")


repository_path = 'C:/GitHub_Demo/Bioinformatics'

res = stchk(repository_path)

if res == "NO":
	print("You did not make any changes or modifications.")
else:
	print("\n********** Mentioning the name and modifications are mandatory. **********\n")
	prnm = input("Enter your name: ")
	print ("\n")
	chn = input("Describe changes done (Modification, Addition, Deletion etc.): ")
	print ("\n")
	commit_message = prnm + ":" + "\t" + chn
	if (pat := re.match(r".+:\t.+", str(commit_message), re.IGNORECASE)):
		git_commit_and_push(repository_path, commit_message)
	else:
		print ("Change/s are not updated to GitHub:  Please ensure that the name and modifications are properly mentioned.")

