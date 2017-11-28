
import subprocess
import os
import shutil 
def test_pr():
	start = str(os.getcwd())
	os.makedirs("test3")
	os.chdir(os.getcwd() + "/test3")
	p = subprocess.Popen(["git", "clone", "https://github.com/machine-shop/test_repo.git"])
	p.communicate()
	os.chdir(os.getcwd() + "/test_repo")

	command = subprocess.Popen(["git", "hub", "pr", "1"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	assert str(command.stdout.read()) == 'Branch pr/1 set up to track remote branch test from ttran428.\n'
	
	# os.chdir("../..")
	# shutil.rmtree("test3")

def test_pr_out_of_bounds():
	command = subprocess.Popen(["git", "hub", "pr", "3"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	assert "There is no pr with number 3." in str(command.stdout.read())
def test_push():
	# start = str(os.getcwd())
	# os.makedirs("test3")
	# os.chdir(os.getcwd() + "/test3")
	# p = subprocess.Popen(["git", "clone", "https://github.com/machine-shop/test_repo.git"])
	# p.communicate()
	# os.chdir(os.getcwd() + "/test_repo")

	with open("teddy.txt", "w") as f:
		f.write("testing testing...")
	subprocess.Popen(["git", "add", "teddy.txt"])
	subprocess.Popen(["git", "commit", "-m", "local tests"])
	p = subprocess.Popen(["git", "hub", "push"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	assert str(p.stdout.read()) == ""

	os.chdir("../..") #deletes all of the files 
	shutil.rmtree("test3")

def test_push_before_pull():
	start = str(os.getcwd())
	os.makedirs("test3")
	os.chdir(os.getcwd() + "/test3")
	p = subprocess.Popen(["git", "clone", "https://github.com/machine-shop/test_repo.git"])
	p.communicate()
	os.chdir(os.getcwd() + "/test_repo")

	with open("teddy.txt", "w") as f:
		f.write("testing testing...")
	subprocess.Popen(["git", "add", "teddy.txt"])
	subprocess.Popen(["git", "commit", "-m", "local tests"])
	p = subprocess.Popen(["git", "hub", "push"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	assert "This command must be used after git hub pr" in str(p.stdout.read()) 

	os.chdir("../..") #deletes all of the files 
	shutil.rmtree("test3")
