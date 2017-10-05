
import subprocess
def test_git_repo():
	subprocess.Popen(["git", "clone", "git@github.com:machine-shop/test_repo.git"])
	subprocess.Popen(["ls"])
	subprocess.Popen(["cd", "test_repo"])
def test_push():
	assert 5 == 5

def test_pull():
	assert 6 == 6
