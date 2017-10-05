
import subprocess
import os
def test_git_repo():
	os.makedirs("test3")
	os.chdir(os.getcwd() + "/test3")
	p = subprocess.Popen(["git", "clone", "https://github.com/machine-shop/test_repo.git"])
	p.communicate()
	os.chdir(os.getcwd() + "/test_repo")

	print("running new command")
	command = subprocess.Popen(["git", "hub", "pr", "1"], stdout=subprocess.PIPE, stdin = subprocess.PIPE)
	print(str(command.stdout.read()))
	


def test_push():
	assert 5 == 5

def test_pull():
	assert 6 == 6
